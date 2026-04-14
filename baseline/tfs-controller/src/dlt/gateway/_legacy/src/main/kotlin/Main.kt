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

import context.ContextOuterClass
import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import dlt.DltGateway
import dlt.DltGatewayServiceGrpcKt
import java.io.Closeable
import java.util.*
import java.util.concurrent.TimeUnit

class DltServiceClient(private val channel: ManagedChannel) : Closeable {
    private val stub: DltGatewayServiceGrpcKt.DltGatewayServiceCoroutineStub =
        DltGatewayServiceGrpcKt.DltGatewayServiceCoroutineStub(channel)

    suspend fun putData(data: DltGateway.DltRecord) {
        println("Sending record ${data.recordId}...")
        val response = stub.recordToDlt(data)
        println("Response: ${response.recordId}")
    }

    suspend fun getData(id: DltGateway.DltRecordId) {
        println("Requesting record $id...")
        val response = stub.getFromDlt(id)
        println("Got data: $response")
    }

    fun subscribe(filter: DltGateway.DltRecordSubscription) {
        val subscription = stub.subscribeToDlt(filter)
        GlobalScope.launch {
            subscription.collect {
                println("Got subscription event")
                println(it)
            }
        }
    }

    override fun close() {
        channel.shutdown().awaitTermination(5, TimeUnit.SECONDS)
    }
}


fun main() = runBlocking {
    val port = 50051
    val channel = ManagedChannelBuilder.forAddress("localhost", port).usePlaintext().build()

    val client = DltServiceClient(channel)

    val domainUuid = UUID.randomUUID().toString()
    val recordUuid = UUID.randomUUID().toString()
    println("New domain uuid $domainUuid")
    println("New record uuid $recordUuid")

    val id = DltGateway.DltRecordId.newBuilder()
        .setDomainUuid(
            ContextOuterClass.Uuid.newBuilder()
                .setUuid(domainUuid)
        )
        .setRecordUuid(
            ContextOuterClass.Uuid.newBuilder()
                .setUuid(recordUuid)
        )
        .setType(DltGateway.DltRecordTypeEnum.DLTRECORDTYPE_SERVICE)
        .build()

    val subscription = DltGateway.DltRecordSubscription.newBuilder()
        .addType(DltGateway.DltRecordTypeEnum.DLTRECORDTYPE_CONTEXT)
        .addType(DltGateway.DltRecordTypeEnum.DLTRECORDTYPE_LINK)
        .addType(DltGateway.DltRecordTypeEnum.DLTRECORDTYPE_SERVICE)
        .addOperation(DltGateway.DltRecordOperationEnum.DLTRECORDOPERATION_ADD)
        .addOperation(DltGateway.DltRecordOperationEnum.DLTRECORDOPERATION_UPDATE)
        .addOperation(DltGateway.DltRecordOperationEnum.DLTRECORDOPERATION_DELETE)
        .build()

    client.subscribe(subscription)

    Thread.sleep(5000)

    val data = DltGateway.DltRecord.newBuilder()
        .setRecordId(id)
        .setOperation(DltGateway.DltRecordOperationEnum.DLTRECORDOPERATION_ADD)
        .setDataJson("\"{\"device_config\": {\"config_rules\": []}, \"device_drivers\": []," +
                "\"device_endpoints\": [], \"device_id\": {\"device_uuid\": {\"uuid\": \"dev-12345\"}}," +
                "\"device_operational_status\": \"DEVICEOPERATIONALSTATUS_ENABLED\"," +
                "\"device_type\": \"packet-router\"}\", \"operation\": \"DLTRECORDOPERATION_ADD\"," +
                "\"record_id\": {\"domain_uuid\": {\"uuid\": \"tfs-a\"}, \"record_uuid\": {\"uuid\": \"dev-12345\"}," +
                "\"type\": \"DLTRECORDTYPE_DEVICE\"}")
        .build()

    println("sending new record")
    client.putData(data)
    client.getData(id)

    Thread.sleep(5000)

    val updateData = DltGateway.DltRecord.newBuilder()
        .setRecordId(id)
        .setOperation(DltGateway.DltRecordOperationEnum.DLTRECORDOPERATION_UPDATE)
        .setDataJson("{\"name\": \"test\"}")
        .build()

    println("updating record")
    client.putData(updateData)
    client.getData(id)

    Thread.sleep(5000)

    val removeData = DltGateway.DltRecord.newBuilder()
        .setRecordId(id)
        .setOperation(DltGateway.DltRecordOperationEnum.DLTRECORDOPERATION_DELETE)
        .setDataJson("{\"name\": \"test\"}")
        .build()

    println("removing record")
    client.putData(removeData)
    try {
        client.getData(id)
    } catch (e: Exception) {
        println(e.toString())
    }
    Thread.sleep(5000)
}
