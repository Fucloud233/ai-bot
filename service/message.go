package service

import (
	"net/http"
	"strconv"

	"example.com/m/v2/model"
	"example.com/m/v2/utils/error"
	"github.com/gin-gonic/gin"
)

func PostMessages(c *gin.Context) {
	// https://go-macaron.com/zh-cn/middlewares/binding#huo-qu-json-shu-ju
	var content struct {
		// Attribute -> database: under_score_case
		// -> json: camelCased
		BotRole string 
		Phone string 
		Messages []model.Message `binding:"dive"`
	}

	// parse content
	err := c.ShouldBindJSON(&content)
	if err != nil {
		c.JSON(http.StatusBadRequest, error.JSONParseError)
		return
	} else if !model.CheckUserExist(content.Phone) {
		// check is exist
		c.JSON(http.StatusNotFound, error.UserNotFound)
		return
	}

	// convert
	messages := []model.Message{}
	for _, msg := range content.Messages {
		msg.BotRole = content.BotRole
		msg.Phone = content.Phone

		messages = append(messages, msg)
	}

	status := http.StatusOK
	if model.AddMessages(&messages) != nil{
		status = http.StatusInternalServerError
	}

	c.JSON(status, "")
}


func GetNewestMessage(c *gin.Context) {
	phone := c.Query("phone")
	n, err := strconv.Atoi(c.Query("n"))

	if phone == ""{
		c.JSON(http.StatusBadRequest, error.ParamLose)
		return
	} else if !model.CheckUserExist(phone) {
		c.JSON(http.StatusNotFound, error.UserNotFound)
		return
	} else if err != nil {
		n = 10
	}

	// convert message to result
	var result struct {
		Messages []model.Message `json:"messages" binding:"dive"`
	}
	var messages []model.Message
	messages, err = model.GetNewestMessage(phone, n)
	result.Messages = messages

	status := http.StatusOK
	if err != nil {
		status = http.StatusBadRequest
	}
	c.IndentedJSON(status, result)
}
