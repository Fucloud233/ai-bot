package service

import (
	"ai-bot/llm"
	"ai-bot/model"
	"ai-bot/utils/error"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func PostMessages(c *gin.Context) {
	// https://go-macaron.com/zh-cn/middlewares/binding#huo-qu-json-shu-ju
	var content struct {
		// Attribute -> database: under_score_case
		// -> json: camelCased
		BotRole  string
		Phone    string
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
	if model.AddMessages(&messages) != nil {
		status = http.StatusInternalServerError
	}

	c.JSON(status, "")
}

func PostMessage(c *gin.Context) {
	var content struct{
		// Messages []llm.Message `binding:"dive"`
		Message llm.Message
		BotRole string
	}
	
	err := c.ShouldBindJSON(&content)
	if err != nil {
		c.JSON(http.StatusBadRequest, error.GetErrorMessage(error.JSONParseError))
	}

	answer := llm.ChatWithRole(content.Message, content.BotRole)

	c.JSON(http.StatusOK, gin.H{
		"message": answer,
	})
	// 搜索向量数据库

	// 获取指定描述的Prompt

	// 合成prompt

	// 添加的到数据库

	// 返回结果
}

func GetNewestMessage(c *gin.Context) {
	phone := c.Query("phone")
	num, err1 := strconv.Atoi(c.Query("num"))
	size, err2 := strconv.Atoi(c.Query("size"))

	if phone == "" {
		c.JSON(http.StatusBadRequest,  error.GetErrorMessage(error.ParamLose))
		return
	} else if !model.CheckUserExist(phone) {
		c.JSON(http.StatusNotFound, error.GetErrorMessage(error.UserNotFound))
		return
	} else if err1 != nil {
		num = 10
	} else if err2 != nil {
		size = 0;
	}

	// convert message to result
	var result struct {
		Messages []model.Message `json:"messages" binding:"dive"`
	}
	messages, err := model.GetNewestMessage(phone, num, size)
	result.Messages = messages

	status := http.StatusOK
	if err != nil {
		status = http.StatusBadRequest
	}
	c.IndentedJSON(status, result)
}


