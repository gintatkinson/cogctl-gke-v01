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

CC       = gcc
CFLAGS   = -I. -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include/
LDLIBS   = -lm
LDFLAGS  = 

all: pathComp

release: CFLAGS += -O6 -Wall -DPOSIX_SOURCE
release: pathComp

debug: CFLAGS  += -O0 -ggdb -g -DDEBUG
debug: LDFLAGS += -g
debug: pathComp-dbg

coverage: CFLAGS  += -O0 -ggdb -g -DDEBUG -fprofile-arcs -ftest-coverage -DGCOV
coverage: LDFLAGS += -g -lgcov --coverage -fprofile-arcs -ftest-coverage -DGCOV
coverage: pathComp-cvr

pathComp: pathComp.o pathComp_log.o pathComp_cjson.o pathComp_tools.o pathComp_ksp.o pathComp_sp.o pathComp_ear.o pathComp_RESTapi.o 
	gcc -o pathComp pathComp.o pathComp_log.o pathComp_cjson.o pathComp_tools.o pathComp_ksp.o pathComp_sp.o pathComp_ear.o pathComp_RESTapi.o \
		-L/usr/lib/x86_64-linux-gnu/ -lglib-2.0 -luuid $(LDFLAGS) $(LDLIBS)

pathComp-dbg: pathComp.o pathComp_log.o pathComp_cjson.o pathComp_tools.o pathComp_ksp.o pathComp_sp.o pathComp_ear.o pathComp_RESTapi.o 
	gcc -o pathComp-dbg pathComp.o pathComp_log.o pathComp_cjson.o pathComp_tools.o pathComp_ksp.o pathComp_sp.o pathComp_ear.o pathComp_RESTapi.o \
		-L/usr/lib/x86_64-linux-gnu/ -lglib-2.0 -luuid $(LDFLAGS) $(LDLIBS)

pathComp-cvr: pathComp.o pathComp_log.o pathComp_cjson.o pathComp_tools.o pathComp_ksp.o pathComp_sp.o pathComp_ear.o pathComp_RESTapi.o 
	gcc -o pathComp-cvr pathComp.o pathComp_log.o pathComp_cjson.o pathComp_tools.o pathComp_ksp.o pathComp_sp.o pathComp_ear.o pathComp_RESTapi.o \
		-L/usr/lib/x86_64-linux-gnu/ -lglib-2.0 -luuid $(LDFLAGS) $(LDLIBS)

pathComp_log.o: pathComp_log.h pathComp_log.c
	$(CC) $(CFLAGS) -c pathComp_log.c -o pathComp_log.o  

pathComp_cjson.o: pathComp_log.h pathComp_cjson.h pathComp_cjson.c
	$(CC) $(CFLAGS) -c pathComp_cjson.c -o pathComp_cjson.o  
	
pathComp_tools.o: pathComp_log.h pathComp_tools.h pathComp_tools.c
	$(CC) $(CFLAGS) -c pathComp_tools.c -o pathComp_tools.o  
	
pathComp_ksp.o: pathComp_log.h pathComp_tools.h pathComp_ksp.h pathComp_ksp.c
	$(CC) $(CFLAGS) -c pathComp_ksp.c -o pathComp_ksp.o

pathComp_sp.o: pathComp_log.h pathComp_tools.h pathComp_sp.h pathComp_sp.c
	$(CC) $(CFLAGS) -c pathComp_sp.c -o pathComp_sp.o

pathComp_ear.o: pathComp_log.h pathComp_tools.h pathComp_ear.h pathComp_ear.c
	$(CC) $(CFLAGS) -c pathComp_ear.c -o pathComp_ear.o
	
pathComp_RESTapi.o: pathComp_tools.h pathComp_log.h pathComp_cjson.h pathComp_ksp.h pathComp_sp.h pathComp_ear.h pathComp_RESTapi.h pathComp_RESTapi.c
	$(CC) $(CFLAGS) -c pathComp_RESTapi.c -o pathComp_RESTapi.o

pathComp.o: pathComp_log.h pathComp_RESTapi.h pathComp.c pathComp.h
	$(CC) $(CFLAGS) -c pathComp.c -o pathComp.o 

clean:	
	rm -f *.o *.gcno *.gcda *.gcov *.log pathComp pathComp-dbg pathComp-cvr
