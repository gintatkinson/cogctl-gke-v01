/*
SPDX-License-Identifier: Apache-2.0
*/
package fabric

import org.hyperledger.fabric.gateway.Identities
import org.hyperledger.fabric.gateway.Wallet
import org.hyperledger.fabric.gateway.X509Identity
import org.hyperledger.fabric.sdk.Enrollment
import org.hyperledger.fabric.sdk.User
import org.hyperledger.fabric_ca.sdk.HFCAClient
import org.hyperledger.fabric_ca.sdk.RegistrationRequest
import java.security.PrivateKey

fun registerUser(config: proto.Config.DltConfig, caClient: HFCAClient, wallet: Wallet) {
    // Check to see if we've already enrolled the user.
    if (wallet[config.user] != null) {
        println("An identity for the user ${config.user} already exists in the wallet")
        return
    }
    val adminIdentity = wallet[config.caAdmin] as X509Identity
    val admin = object : User {
        override fun getName(): String {
            return config.caAdmin
        }

        override fun getRoles(): Set<String>? {
            return null
        }

        override fun getAccount(): String? {
            return null
        }

        override fun getAffiliation(): String {
            return config.affiliation
        }

        override fun getEnrollment(): Enrollment {
            return object : Enrollment {
                override fun getKey(): PrivateKey {
                    return adminIdentity.privateKey
                }

                override fun getCert(): String {
                    return Identities.toPemString(adminIdentity.certificate)
                }
            }
        }

        override fun getMspId(): String {
            return config.msp
        }
    }

    // Register the user, enroll the user, and import the new identity into the wallet.
    val registrationRequest = RegistrationRequest(config.user)
    registrationRequest.affiliation = config.affiliation
    registrationRequest.enrollmentID = config.user
    val enrollmentSecret = caClient.register(registrationRequest, admin)
    val enrollment = caClient.enroll(config.user, enrollmentSecret)
    val user = Identities.newX509Identity(config.msp, enrollment)
    wallet.put(config.user, user)
    println("Successfully enrolled user ${config.user} and imported it into the wallet")
}
