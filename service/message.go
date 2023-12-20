package service

import (
	"ai-bot/llm"
	"ai-bot/model"
	"ai-bot/utils/error"
	"net/http"
	"strconv"
	"time"

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

// the history messages in the frontend is different with backend
// listener metrics: many messages will be merge into one message
func PostMessage(c *gin.Context) {
	var content struct{
		Message string
		BotRole string
		Phone string
		Duration int
	}

	sendTime := time.Now()
	err := c.ShouldBindJSON(&content)
	if err != nil {
		c.JSON(http.StatusBadRequest, error.GetErrorMessage(error.JSONParseError))
	} else if !model.CheckUserExist(content.Phone) {
		c.JSON(http.StatusNotFound, error.GetErrorMessage(error.UserNotFound))
		return
	}
	
	// 1. get the description prompt
	rolePrompt, err := model.GetRolePrompt(content.Phone, content.BotRole)
	if err != nil {
		rolePrompt = ""
	}

	// 2. search history from newest database
	historyMessages, err := model.GetNewestMessage(content.Phone, 10, 0, content.Duration);
	if err != nil {
		historyMessages = []model.Message{}
	} else if len(historyMessages) >= 2 {
		begin := 0
		end := len(historyMessages)
		if historyMessages[0].Role != model.User {
			begin += 1
		} 
		if historyMessages[len(historyMessages)-1].Role != model.Assistant {
			end -= 1
		}
		if begin > end {
			historyMessages = []model.Message{}
		} else {
			historyMessages = historyMessages[begin:end]
		}
	}

	// 3. TODO: search history from vector database
	// relatedHistoryMessages, err := 

	// 4. call LLM
	answer := llm.ChatWithRole(content.BotRole, rolePrompt, historyMessages, content.Message)
	answerTime := time.Now()
	
	// 5. save to database
	messagesToSave := []model.Message{
		model.NewMessage(content.Phone, content.BotRole, model.User, content.Message, sendTime),
		model.NewMessage(content.Phone, content.BotRole, model.Assistant, answer, answerTime),
	}
	err = model.AddMessages(&messagesToSave)
	if err != nil {
		c.JSON(http.StatusInternalServerError, nil)
		return;
	}

	c.JSON(http.StatusOK, gin.H{
		"message": answer,
	})
}

func GetNewestMessage(c *gin.Context) {
	phone := c.Query("phone")
	num, err1 := strconv.Atoi(c.Query("num"))
	offset, err2 := strconv.Atoi(c.Query("offset"))

	if phone == "" {
		c.JSON(http.StatusBadRequest,  error.GetErrorMessage(error.ParamLose))
		return
	} else if !model.CheckUserExist(phone) {
		c.JSON(http.StatusNotFound, error.GetErrorMessage(error.UserNotFound))
		return
	} else if err1 != nil {
		num = 10
	} else if err2 != nil {
		offset = 0
	}

	// convert message to result
	var result struct {
		Messages []model.Message `json:"messages" binding:"dive"`
	}
	messages, err := model.GetMessages(phone, num, offset)
	result.Messages = messages

	status := http.StatusOK
	if err != nil {
		status = http.StatusBadRequest
	}
	c.IndentedJSON(status, result)
}

func DeleteAllMessages(c *gin.Context) {
	var content struct{
		Phone string
		BotRole string
	}

	err := c.ShouldBindJSON(&content)
	if err != nil {
		c.JSON(http.StatusBadRequest, error.GetErrorMessage(error.JSONParseError))
		return
	} 

	err = model.DeleteAllMessages(content.Phone, content.BotRole)
	status := http.StatusOK
	if err != nil {
		status = http.StatusInternalServerError
	}

	c.JSON(status, nil)
}

