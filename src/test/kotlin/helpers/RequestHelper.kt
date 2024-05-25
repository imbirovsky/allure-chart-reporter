package helpers

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.databind.SerializationFeature
import helpers.AllureHelper.updateTestNameForAllureReport
import io.qameta.allure.restassured.AllureRestAssured
import io.restassured.RestAssured
import io.restassured.response.ValidatableResponse
import io.restassured.specification.RequestSpecification

// This object contains helper methods for sending HTTP requests
object RequestHelper {

    // This method prepares a request with AllureRestAssured filter and logs all interactions
    private fun sendRequest(): RequestSpecification {
        return RestAssured.given().filter(AllureRestAssured()).log().all()
    }

    // This method prepares a request with a body, AllureRestAssured filter and logs all interactions
    private fun sendRequest(body: String = ""): RequestSpecification {
        return RestAssured.given().filter(AllureRestAssured()).log().all().body(body)
    }

    // This method sends a GET request to the provided URL and validates the response
    // updateTestNameForAllureReport - adds the request URL to the test name
    fun sendGetRequest(requestUrl: String, code: Int = 200, contentType: String = "application/json"): ValidatableResponse {
        updateTestNameForAllureReport("\n$requestUrl")
        val response = sendRequest().contentType(contentType).get(requestUrl).then()
        logResponse(response)
        response.statusCode(code)
        return response
    }

    // This method sends a POST request to the provided URL with the provided body and validates the response
    fun sendPostRequest(requestUrl: String, body: String, code: Int = 200, contentType: String = "application/json"): ValidatableResponse {
        updateTestNameForAllureReport("\n$requestUrl without body")
        val response = sendRequest(body).contentType(contentType).post(requestUrl).then()
        logResponse(response)
        response.statusCode(code)
        return response
    }

    // This method logs the response details
    private fun logResponse(response: ValidatableResponse) {
        val contentType = response.extract().contentType()
        val statusCode = response.extract().statusCode()
        val colorCode = if (statusCode == 200 || statusCode == 202) "\u001B[32m" else "\u001B[31m"
        val logBuilder = StringBuilder()
        logBuilder.append("\u001B[1m\n-----------------------------------------------------------\n\u001B[0m\n")
        logBuilder.append("\u001B[1mStatus code: $colorCode$statusCode\u001B[0m\n")

        if (contentType.contains("application/json")) {
            val responseAsString = response.extract().asString()
            val mapper = ObjectMapper().enable(SerializationFeature.WRITE_BIGDECIMAL_AS_PLAIN)
            val jsonNode = mapper.readTree(responseAsString)
            val json = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(jsonNode)
            logBuilder.append(json)
        } else {
            logBuilder.append(response.extract().asString())
        }
        println(logBuilder.toString())
    }

}