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
//          Copyright (c) 2021 NEC Laboratories Europe GmbH
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

import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

import com.google.protobuf.gradle.generateProtoTasks
import com.google.protobuf.gradle.id
import com.google.protobuf.gradle.plugins
import com.google.protobuf.gradle.protobuf
import com.google.protobuf.gradle.protoc

ext["grpcVersion"] = "1.47.0"
ext["grpcKotlinVersion"] = "1.3.0" // CURRENT_GRPC_KOTLIN_VERSION
ext["protobufVersion"] = "3.20.1"
ext["ktorVersion"] = "1.6.5"

plugins {
    kotlin("jvm") version "1.6.21"
    kotlin("plugin.serialization") version "1.4.21"
    id("com.google.protobuf") version "0.8.18"
    application
}

group = "eu.neclab"
version = "1.0-SNAPSHOT"

repositories {
    mavenLocal()
    google()
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib-jdk8"))
    testImplementation("org.jetbrains.kotlin:kotlin-test:1.6.21")
    implementation("javax.annotation:javax.annotation-api:1.3.2")
    implementation("io.grpc:grpc-kotlin-stub:1.3.0")
    implementation("io.grpc:grpc-protobuf:1.47.0")
    implementation("com.google.protobuf:protobuf-kotlin:3.21.1")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.3")
    implementation("org.hyperledger.fabric:fabric-gateway-java:2.2.5")
    implementation("ch.qos.logback:logback-classic:1.2.11")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.3.1")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-protobuf:1.3.1")
    runtimeOnly("io.grpc:grpc-netty:${rootProject.ext["grpcVersion"]}")
}

tasks.test {
    useJUnitPlatform()
}

tasks.withType<KotlinCompile> {
    kotlinOptions.jvmTarget = "11"
}

tasks.withType<KotlinCompile>().all {
    kotlinOptions {
        freeCompilerArgs = listOf("-Xopt-in=kotlin.RequiresOptIn")
    }
}


application {
    mainClass.set("MainKt")
}

task("runServer", JavaExec::class) {
    main = "grpc.FabricServerKt"
    classpath = sourceSets["main"].runtimeClasspath
}


sourceSets {
    main {
        proto {
            srcDir("proto")
            srcDir("src/main/kotlin/proto")
        }
    }
}

sourceSets {
    val main by getting { }
    main.java.srcDirs("build/generated/source/proto/main/grpc")
    main.java.srcDirs("build/generated/source/proto/main/grpckt")
    main.java.srcDirs("build/generated/source/proto/main/java")
    main.java.srcDirs("build/generated/source/proto/main/kotlin")
}

protobuf {
    protoc {
        artifact = "com.google.protobuf:protoc:${rootProject.ext["protobufVersion"]}"
    }
    plugins {
        id("grpc") {
            artifact = "io.grpc:protoc-gen-grpc-java:${rootProject.ext["grpcVersion"]}"
        }
        id("grpckt") {
            artifact = "io.grpc:protoc-gen-grpc-kotlin:${rootProject.ext["grpcKotlinVersion"]}:jdk8@jar"
        }
    }
    generateProtoTasks {
        all().forEach {
            it.plugins {
                id("grpc")
                id("grpckt")
            }
            it.builtins {
                id("kotlin")
            }
        }
    }
}
