package service

import (
	"net/http"

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
	} 

	// check is exist
	user := model.UserBasic{ Phone: content.Phone}
	if !user.CheckExist() {
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