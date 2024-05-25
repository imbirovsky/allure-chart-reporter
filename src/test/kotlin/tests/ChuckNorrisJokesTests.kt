package tests

import constants.Constants.API.ACTION
import constants.Constants.API.CATEGORY
import constants.Constants.API.HTTPS
import constants.Constants.API.RANDOM
import constants.Constants.API.URL
import constants.Constants.Categories.ANIMAL
import constants.Constants.Categories.CELEBRITY
import constants.Constants.Categories.DEV
import constants.Constants.Categories.FOOD
import constants.Constants.Categories.HISTORY
import constants.Constants.Categories.MOVIE
import constants.Constants.Categories.MUSIC
import constants.Constants.Categories.SPORT
import helpers.RequestHelper.sendGetRequest
import io.qameta.allure.Description
import io.qameta.allure.Epic
import io.restassured.module.jsv.JsonSchemaValidator.matchesJsonSchemaInClasspath
import org.hamcrest.Matchers.equalTo
import org.hamcrest.Matchers.hasItem
import org.testng.SkipException
import org.testng.annotations.DataProvider
import org.testng.annotations.Test

// This class contains tests for Chuck Norris Jokes API. Tests are written using TestNG and Rest Assured
@Epic("Chuck Norris Jokes Status Tests")
class ChuckNorrisJokesTests {

    // Base request data for the API
    private val requestData = "${HTTPS}${URL}${ACTION}${RANDOM}"
    // Expected icon URL in the response
    private val iconUrl = "https://assets.chucknorris.host/img/avatar/chuck-norris.png"

    // Test to get a joke from Chuck with a specific category
    @Description("Get a joke from Chuck with category (description)")
    @Test(dataProvider = "categories")
    fun `Joke from Chuck with category`(category: String) {
        sendGetRequest("$requestData?$CATEGORY$category")
            .body("icon_url", equalTo(iconUrl))
            .body("categories", hasItem(category))
            .body(matchesJsonSchemaInClasspath("json_schemes/chucknorris_jokes.json"))
            .statusCode(200)
    }

    // Test to get a random joke from Chuck
    @Description("Get a random joke from Chuck (description)")
    @Test
    fun `Random joke from Chuck`() {
        sendGetRequest(requestData)
            .body("icon_url", equalTo(iconUrl))
            .body(matchesJsonSchemaInClasspath("json_schemes/chucknorris_jokes.json"))
            .statusCode(200)
    }

    // Test to simulate a broken test case
    @Description("Get a joke from Chuck | broken (description)")
    @Test
    fun `Joke from Chuck (broken)`() {
        throw RuntimeException("This test is broken")
        @Suppress("UNREACHABLE_CODE")
        sendGetRequest(requestData)
            .body("icon_url", equalTo(iconUrl))
            .body(matchesJsonSchemaInClasspath("json_schemes/chucknorris_jokes.json"))
            .statusCode(200)
    }

    // Test to simulate a skipped test case
    @Description("Get a joke from Chuck | skip (description)")
    @Test
    fun `Joke from Chuck (skipped)`() {
        throw SkipException("Skipping this test")
        @Suppress("UNREACHABLE_CODE")
        sendGetRequest(requestData)
            .body("icon_url", equalTo(iconUrl))
            .body(matchesJsonSchemaInClasspath("json_schemes/chucknorris_jokes.json"))
            .statusCode(200)
    }

    // Test to simulate a failed test case
    @Description("Get a joke from Chuck | failed (description)")
    @Test
    fun `Joke from Chuck (failed)`() {
        sendGetRequest("$requestData/$DEV")
            .statusCode(200)
    }

    // Data provider for the categories
    @DataProvider(name = "categories")
    fun categoryList(): Array<String> {
        return arrayOf(
            ANIMAL,
            CELEBRITY,
            DEV,
            FOOD,
            HISTORY,
            MOVIE,
            MUSIC,
            SPORT
        )
    }

}