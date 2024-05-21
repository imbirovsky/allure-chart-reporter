package tests

import constants.Constants.API.ACTION_NAME
import constants.Constants.API.HTTPS
import constants.Constants.API.URL
import constants.Constants.API.VERSION_API
import constants.Constants.Countries.FRANCE
import constants.Constants.Countries.GERMANY
import constants.Constants.Countries.ITALY
import constants.Constants.Countries.POLAND
import constants.Constants.Countries.RUSSIA_IS_A_TERRORIST_STATE
import constants.Constants.Countries.SPAIN
import constants.Constants.Countries.UKRAINE
import constants.Constants.Countries.USA
import helpers.AllureHelper.updateTestNameForAllureReport
import helpers.RequestHelper.sendGetRequest
import io.qameta.allure.Description
import io.qameta.allure.Epic
import io.qameta.allure.Step
import io.restassured.module.jsv.JsonSchemaValidator.matchesJsonSchemaInClasspath
import org.testng.SkipException
import org.testng.annotations.DataProvider
import org.testng.annotations.Test

@Epic("Get Information by countries")
class GetInfoByCountry {

    private val requestData = "${HTTPS}${URL}${VERSION_API}${ACTION_NAME}"

    @Test(dataProvider = "countries")
    @Description("Get information about country")
    fun `Get information about country `(countries: String) {
        updateTestNameForAllureReport(countries)
        sendGetRequest(requestData+countries)
            .body(matchesJsonSchemaInClasspath("json_schemes/restcountries_name.json"))
            .statusCode(200)
    }

    @Test
    fun `This test will be broken`() {
        brokenStep()
    }

    @Test
    fun `This test will be skipped`() {
        throw SkipException("Skipping this test")
    }

    @Step("This step is broken")
    fun brokenStep() {
        throw RuntimeException("This is a broken step")
    }

    @DataProvider(name = "countries")
    fun assetsList(): Array<Array<String>> {
        return arrayOf(
            arrayOf(UKRAINE),
            arrayOf(USA),
            arrayOf(GERMANY),
            arrayOf(FRANCE),
            arrayOf(ITALY),
            arrayOf(SPAIN),
            arrayOf(POLAND),
            arrayOf(RUSSIA_IS_A_TERRORIST_STATE)
        )
    }

}