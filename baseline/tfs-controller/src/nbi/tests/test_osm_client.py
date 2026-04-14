#!/usr/bin/env python3
# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import time, requests, statistics, sys
import matplotlib.pyplot as plt
from collections import deque

BASE_URL = "http://127.0.0.1/osm-api"   # TFS NBI OSM-Client API entry point
NST_NAME = "sonic-ns-slice"
ACCOUNT  = "openstack-site"
SSH_KEY  = ""
CONFIG   = ""
ITER     = 15                 # number of loops
POLL_S   = 0.5                # poll interval only for refilling ID (not timed)
MAX_WAIT = 180.0

sess = requests.Session()
sess.headers.update({"Accept": "application/json"})

# ---------- helpers ----------
def q(samples, p):
    if not samples: return None
    xs = sorted(samples); k = (len(xs)-1) * (p/100.0)
    f = int(k); c = min(f+1, len(xs)-1)
    return xs[f] if f==c else xs[f]*(c-k) + xs[c]*(k-f)

def pctline(label, arr):
    if not arr: return f"{label}: no samples"
    return (f"{label}: n={len(arr)}  mean={statistics.fmean(arr):.3f}s  "
            f"p50={q(arr,50):.3f}s  p90={q(arr,90):.3f}s  p99={q(arr,99):.3f}s")

def ecdf(arr):
    xs = sorted(arr)
    n = len(xs)
    ys = [i / n for i in range(1, n+1)]
    return xs, ys

# ---------- API calls ----------
def list_ids():
    r = sess.get(f"{BASE_URL}/NS_Services", timeout=15)
    r.raise_for_status()
    return r.json().get("id", [])

def get_name(nsi_id):
    r = sess.get(f"{BASE_URL}/NS_Service/{nsi_id}", timeout=15)
    r.raise_for_status()
    return (r.json().get("nsi") or {}).get("nsi_name")

def get_nsi(nsi_id):
    t0 = time.monotonic()
    r = sess.get(f"{BASE_URL}/NS_Service/{nsi_id}", timeout=30)
    dt = time.monotonic() - t0
    r.raise_for_status()
    return dt

def delete_nsi(nsi_id):
    t0 = time.monotonic()
    r = sess.delete(f"{BASE_URL}/NS_Service/{nsi_id}", timeout=60)
    dt = time.monotonic() - t0
    r.raise_for_status()
    ok = bool(r.json().get("succeded", False))
    return ok, dt

def create_nsi(name):
    payload = {"nst_name": NST_NAME, "nsi_name": name,
               "config": CONFIG, "ssh_key": SSH_KEY, "account": ACCOUNT}
    t0 = time.monotonic()
    r = sess.post(f"{BASE_URL}/NS_Services", json=payload, timeout=30)
    dt = time.monotonic() - t0
    r.raise_for_status()
    ok = bool(r.json().get("succeded", False))
    return ok, dt

def resolve_id_by_name(target):
    """Refill pool after create; NOT timed (kept out of metrics)."""
    deadline = time.monotonic() + MAX_WAIT
    while time.monotonic() < deadline:
        for nid in list_ids():
            try:
                if get_name(nid) == target:
                    return nid
            except Exception:
                pass
        time.sleep(POLL_S)
    return None

# ---------- main ----------
def main():
    # Seed a pool of IDs to consume
    pool = deque(list_ids())
    if not pool:
        # create one so we can start
        seed = f"bench-seed-{int(time.time())}"
        ok, _ = create_nsi(seed)
        if not ok:
            print("Failed to seed an NSI; aborting.")
            sys.exit(1)
        nid = resolve_id_by_name(seed)
        if not nid:
            print("Seed NSI not visible; aborting.")
            sys.exit(1)
        pool.append(nid)

    get_t, del_t, create_t = [], [], []

    for i in range(1, ITER+1):
        # If pool is empty, list again
        if not pool:
            pool.extend(list_ids())
            if not pool:
                print(f"[{i}] No IDs available to GET/DELETE; creating one…")
                tmpname = f"bench-tmp-{int(time.time())}-{i}"
                ok, _ = create_nsi(tmpname)
                nid = resolve_id_by_name(tmpname)
                if nid: pool.append(nid)
                else:
                    print("  still no ID; skipping iteration.")
                    continue

        current_id = pool.popleft()

        # GET (timed)
        try:
            dt = get_nsi(current_id)
            print(f"[{i}] get {current_id}: {dt:.3f}s OK")
            get_t.append(dt)
        except Exception as e:
            print(f"[{i}] get {current_id}: ERROR ({e}); skipping delete")
            continue

        # DELETE (timed)
        try:
            ok, ddt = delete_nsi(current_id)
            print(f"    delete {current_id}: {ddt:.3f}s {'OK' if ok else 'NOTOK'}")
            if ok: del_t.append(ddt)
        except Exception as e:
            print(f"    delete {current_id}: ERROR ({e})")

        # CREATE (timed)
        newname = f"bench-{int(time.time())}-{i}"
        ok, cdt = create_nsi(newname)
        print(f"    create {newname}: {cdt:.3f}s {'OK' if ok else 'NOTOK'}")
        if ok: create_t.append(cdt)

        # Refill with the new ID (NOT timed)
        nid = resolve_id_by_name(newname)
        if nid:
            pool.append(nid)
        else:
            print("    (note) new NSI not visible yet; pool not refilled this round")

    # -------- Summary prints --------
    print("\n=== CDF summary (GET → DELETE → CREATE) ===")
    print(pctline("GET", get_t))
    print(pctline("DELETE", del_t))
    print(pctline("CREATE", create_t))

    # -------- ECDF plots --------
    plt.figure()
    if get_t:
        x,y = ecdf(get_t);    plt.step(x,y, where="post", label="GET")
    if del_t:
        x,y = ecdf(del_t);    plt.step(x,y, where="post", label="DELETE")
    if create_t:
        x,y = ecdf(create_t); plt.step(x,y, where="post", label="CREATE")
    plt.xlabel("Time (s)"); plt.ylabel("CDF")
    plt.title(f"Empirical CDF (GET/DELETE/CREATE) n={len(get_t)}")
    plt.grid(True, linestyle=":")
    plt.legend(); plt.tight_layout()
    plt.savefig("ecdf_gdc.png")

    plt.figure()
    if get_t:    plt.step(*ecdf(get_t),    where="post", label="GET")
    if del_t:    plt.step(*ecdf(del_t),    where="post", label="DELETE")
    if create_t: plt.step(*ecdf(create_t), where="post", label="CREATE")
    plt.xlim(0.0, 1.0); plt.ylim(0.0, 1.0)
    plt.xlabel("Time (s)"); plt.ylabel("CDF")
    plt.title("ECDF (zoom 0–1s)")
    plt.grid(True, linestyle=":"); plt.legend(); plt.tight_layout()
    plt.savefig("ecdf_gdc_zoom.png")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
