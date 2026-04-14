/*
 * Copyright IBM Corp. All Rights Reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

package fabric

import org.hyperledger.fabric.gateway.Identities
import org.hyperledger.fabric.gateway.Wallet
import org.hyperledger.fabric_ca.sdk.EnrollmentRequest
import org.hyperledger.fabric_ca.sdk.HFCAClient

fun enrollAdmin(config: proto.Config.DltConfig, caClient: HFCAClient, wallet: Wallet) {
    // Check to see if we've already enrolled the admin user.
    if (wallet.get(config.caAdmin) != null) {
        println("An identity for the admin user ${config.caAdmin} already exists in the wallet")
        return
    }

    // Enroll the admin user, and import the new identity into the wallet.
    val enrollmentRequestTLS = EnrollmentRequest()
    enrollmentRequestTLS.addHost(config.caUrl)
    enrollmentRequestTLS.profile = "tls"
    val enrollment = caClient.enroll(config.caAdmin, config.caAdminSecret, enrollmentRequestTLS)
    val user = Identities.newX509Identity(config.msp, enrollment)
    wallet.put(config.caAdmin, user)
    println("Successfully enrolled user ${config.caAdmin} and imported it into the wallet")
}
