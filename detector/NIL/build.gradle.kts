plugins {
    kotlin("jvm") version "2.0.0"
    id("com.github.johnrengelman.shadow") version "8.1.1"
    id("antlr")

    application
}

java.sourceCompatibility = JavaVersion.VERSION_17	

repositories {
    mavenCentral()
}

dependencies {
    // Use RxKotlin
    implementation("io.reactivex.rxjava3:rxkotlin:3.0.1")

    // Use Logger
    implementation("ch.qos.logback:logback-classic:1.4.12")

    // Use JDT
    implementation("org.eclipse.jdt:org.eclipse.jdt.core:3.37.0")

    // Use the Kotlin test library.
    testImplementation("org.jetbrains.kotlin:kotlin-test")

    // Use the Kotlin JUnit integration.
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit")

    // Use ANTLR
    antlr("org.antlr:antlr4:4.9")
}

application {
    mainClass.set("jp.ac.osaka_u.sdl.nil.NILMainKt")
}

tasks.generateGrammarSource {
    enabled = false
}

tasks.generateTestGrammarSource {
    enabled = false
}
