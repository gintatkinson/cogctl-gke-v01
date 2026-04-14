//     NEC Laboratories Europe GmbH
//
//     PROPRIETARY INFORMATION
//
// The software and its source code contain valuable trade secrets and
// shall be maintained in confidence and treated as confidential
// information. The software may only be used for evaluation and/or
// testing purposes, unless otherwise explicitly stated in a written
// agreement with NEC Laboratories Europe GmbH.
//
// Any unauthorized publication, transfer to third parties or
// duplication of the object or source code - either totally or in
// part - is strictly prohibited.
//
//          Copyright (c) 2022 NEC Laboratories Europe GmbH
//          All Rights Reserved.
//
// Authors: Konstantin Munichev <konstantin.munichev@neclab.eu>
//
//
// NEC Laboratories Europe GmbH DISCLAIMS ALL WARRANTIES, EITHER
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES
// OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE AND THE
// WARRANTY AGAINST LATENT DEFECTS, WITH RESPECT TO THE PROGRAM AND
// THE ACCOMPANYING DOCUMENTATION.
//
// NO LIABILITIES FOR CONSEQUENTIAL DAMAGES: IN NO EVENT SHALL NEC
// Laboratories Europe GmbH or ANY OF ITS SUBSIDIARIES BE LIABLE FOR
// ANY DAMAGES WHATSOEVER (INCLUDING, WITHOUT LIMITATION, DAMAGES FOR
// LOSS OF BUSINESS PROFITS, BUSINESS INTERRUPTION, LOSS OF
// INFORMATION, OR OTHER PECUNIARY LOSS AND INDIRECT, CONSEQUENTIAL,
// INCIDENTAL, ECONOMIC OR PUNITIVE DAMAGES) ARISING OUT OF THE USE OF
// OR INABILITY TO USE THIS PROGRAM, EVEN IF NEC Laboratories Europe
// GmbH HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
//
// THIS HEADER MAY NOT BE EXTRACTED OR MODIFIED IN ANY WAY.

package fabric

import context.ContextOuterClass
import dlt.DltGateway.DltRecord
import dlt.DltGateway.DltRecordEvent
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.runBlocking
import org.hyperledger.fabric.gateway.Contract
import org.hyperledger.fabric.gateway.ContractEvent
import org.hyperledger.fabric.gateway.Wallet
import org.hyperledger.fabric.gateway.Wallets
import org.hyperledger.fabric.sdk.security.CryptoSuiteFactory
import org.hyperledger.fabric_ca.sdk.HFCAClient
import proto.Config
import java.nio.file.Paths
import java.util.*
import java.util.function.Consumer

class FabricConnector(val config: Config.DltConfig) {
    private val caClient: HFCAClient
    private val wallet: Wallet
    private val contract: Contract

    private val channels: MutableList<Channel<DltRecordEvent>> = mutableListOf()

    private val encoder: Base64.Encoder = Base64.getEncoder()
    private val decoder: Base64.Decoder = Base64.getDecoder()

    init {
        // Create a CA client for interacting with the CA.
        val props = Properties()
        props["pemFile"] = config.caCertFile
        props["allowAllHostNames"] = "true"
        caClient = HFCAClient.createNewInstance(config.caUrl, props)
        val cryptoSuite = CryptoSuiteFactory.getDefault().cryptoSuite
        caClient.cryptoSuite = cryptoSuite

        // Create a wallet for managing identities
        wallet = Wallets.newFileSystemWallet(Paths.get(config.wallet))
        contract = connect()

        fabricSubscribe()
    }

    private fun fabricSubscribe() {
        val consumer = Consumer { event: ContractEvent? ->
            run {
                println("new event detected")
                val record = DltRecord.parseFrom(decoder.decode(event?.payload?.get()))
                println(record.recordId.recordUuid)
                val eventType: ContextOuterClass.EventTypeEnum = when (event?.name) {
                    "Add" -> ContextOuterClass.EventTypeEnum.EVENTTYPE_CREATE
                    "Update" -> ContextOuterClass.EventTypeEnum.EVENTTYPE_UPDATE
                    "Remove" -> ContextOuterClass.EventTypeEnum.EVENTTYPE_REMOVE
                    else -> ContextOuterClass.EventTypeEnum.EVENTTYPE_UNDEFINED
                }
                val pbEvent = DltRecordEvent.newBuilder()
                    .setEvent(
                        ContextOuterClass.Event.newBuilder()
                            .setTimestamp(
                                ContextOuterClass.Timestamp.newBuilder()
                                    .setTimestamp(System.currentTimeMillis().toDouble())
                            )
                            .setEventType(eventType)
                    )
                    .setRecordId(record.recordId)
                    .build()

                runBlocking {
                    channels.forEach {
                        it.trySend(pbEvent)
                    }
                }
            }
        }
        contract.addContractListener(consumer)
    }

    fun connect(): Contract {
        enrollAdmin(config, caClient, wallet)
        registerUser(config, caClient, wallet)
        return getContract(config, wallet)
    }

    fun putData(record: DltRecord): String {
        println(record.toString())

        try {
            contract.submitTransaction(
                "AddRecord",
                record.recordId.recordUuid.uuid,
                encoder.encodeToString(record.toByteArray())
            )
        } catch (e: Exception) {
            println(e.toString())
            return e.toString()
        }
        return ""
    }

    fun getData(uuid: String): DltRecord {
        return try {
            val result = contract.evaluateTransaction("GetRecord", uuid)
            DltRecord.parseFrom(decoder.decode(result))
        } catch (e: Exception) {
            println(e.toString())
            DltRecord.getDefaultInstance()
        }
    }

    fun updateData(record: DltRecord): String {
        try {
            contract.submitTransaction(
                "UpdateRecord",
                record.recordId.recordUuid.uuid,
                encoder.encodeToString(record.toByteArray())
            )
        } catch (e: Exception) {
            return e.toString()
        }
        return ""
    }

    fun deleteData(record: DltRecord): String {
        try {
            contract.submitTransaction(
                "DeleteRecord",
                record.recordId.recordUuid.uuid,
            )
        } catch (e: Exception) {
            return e.toString()
        }
        return ""
    }

    fun subscribeForEvents(): Channel<DltRecordEvent> {
        val produceCh = Channel<DltRecordEvent>()
        channels.add(produceCh)
        return produceCh
    }
}