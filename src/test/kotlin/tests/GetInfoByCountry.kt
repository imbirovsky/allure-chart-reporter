package tests

import constants.Constants.API.ACTION_NAME
import constants.Constants.API.HTTPS
import constants.Constants.API.URL
import constants.Constants.API.VERSION_API
import constants.Constants.Countries.FRANCE
import constants.Constants.Countries.GERMANY
import constants.Constants.Countries.POLAND
import constants.Constants.Countries.RUSSIA_IS_A_TERRORIST_STATE
import constants.Constants.Countries.SPAIN
import constants.Constants.Countries.UKRAINE
import constants.Constants.Countries.USA
import helpers.RequestHelper.sendGetRequest
import io.qameta.allure.Description
import io.qameta.allure.Epic
import io.restassured.module.jsv.JsonSchemaValidator.matchesJsonSchemaInClasspath
import org.testng.SkipException
import org.testng.annotations.DataProvider
import org.testng.annotations.Test

@Epic("Get Information by countries")
class GetInfoByCountry {

    private val requestData = "${HTTPS}${URL}${VERSION_API}${ACTION_NAME}"

    @Test(dataProvider = "countries")
    @Description("Get information about country")
    fun `Get information about country`(countries: String) {
        sendGetRequest(requestData+countries)
            .body(matchesJsonSchemaInClasspath("json_schemes/restcountries_name.json"))
            .statusCode(200)
    }

    @Test
    fun `Get info about country (failed)`() {
        sendGetRequest(requestData+"ukraine")
            .body(matchesJsonSchemaInClasspath("json_schemes/restcountries_name.json"))
            .statusCode(400)
    }

//    @Test
    fun `Get info about country 2 (failed)`() {
        sendGetRequest(requestData+"usa")
            .body(matchesJsonSchemaInClasspath("json_schemes/restcountries_name.json"))
            .statusCode(303)
    }

    @Test
    fun `This test will be broken`() {
        throw RuntimeException("This is a broken test")
    }

    @Test
    fun `This test will be broken 2`() {
        throw RuntimeException("This is a broken test 2")
    }

    @Test
    fun `This test will be broken 3`() {
        throw RuntimeException("This is a broken test 3")
    }

    @Test
    fun `This test will be broken 4`() {
        throw RuntimeException("This is a broken test 4")
    }

    @Test
    fun `This test will be skipped`() {
        throw SkipException("Skipping this test")
    }

    @Test
    fun `This test will be success`() {
    }

    @Test
    fun `This test will be success 2`() {
    }

    @Test
    fun `This test will be success 3`() {
    }

    @Test
    fun `This test will be success 4`() {
    }

    @Test
    fun `This test will be success 5`() {
    }

    @Test
    fun `This test will be success 6`() {
    }

    @Test
    fun `This test will be success 7`() {
    }

    @Test
    fun `This test will be success 8`() {
    }

    @Test
    fun `This test will be success 9`() {
    }

    @Test
    fun `This test will fail`() {
        throw AssertionError("This test always fails")
    }

    @Test
    fun `This test will fail 2`() {
        throw AssertionError("This test always fails 2")
    }

    @Test
    fun `This test will fail 3`() {
        throw AssertionError("This test always fails 3")
    }

    @Test
    fun `This test will fail 4`() {
        throw AssertionError("This test always fails 4")
    }

    @DataProvider(name = "countries")
    fun assetsList(): Array<Array<String>> {
        return arrayOf(
            arrayOf(UKRAINE),
            arrayOf(USA),
            arrayOf(GERMANY),
            arrayOf(FRANCE),
            arrayOf(SPAIN),
            arrayOf(POLAND),
            arrayOf(RUSSIA_IS_A_TERRORIST_STATE)
        )
    }

}