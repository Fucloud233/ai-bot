package service

import (
	"ai-bot/model"
	"ai-bot/utils/error"
	"net/http"

	"github.com/gin-gonic/gin"
)

func UpdateRolePrompt(c *gin.Context) {
	var rolePrompt model.RolePrompt

	err := c.ShouldBindJSON(&rolePrompt)
	if err != nil {
		c.JSON(http.StatusBadRequest, error.GetErrorMessage(error.JSONParseError))
		return
	} else if !model.CheckUserExist(rolePrompt.Phone) {
		// check is exist
		c.JSON(http.StatusNotFound, error.GetErrorMessage(error.UserNotFound))
		return
	}

	err = rolePrompt.UpdateRolePrompt()
	status := http.StatusOK
	if err != nil {
		status = http.StatusInternalServerError
	}

	c.JSON(status, nil)
}

func GetRolePrompt(c *gin.Context) {
	phone := c.Query("phone")
	botRole := c.Query("botRole")

	if phone == "" || botRole == "" {
		c.JSON(http.StatusBadRequest, error.GetErrorMessage(error.ParamLose))
		return
	} else if !model.CheckUserExist(phone) {
		// check is exist
		c.JSON(http.StatusNotFound, error.UserNotFound)
		return
	}

	rolePrompt, err := model.GetRolePrompt(phone, botRole)
	status := http.StatusOK
	if err != nil {
		status = http.StatusInternalServerError
		c.JSON(status, nil)
	} else {
		c.JSON(status, gin.H{
			"rolePrompt": rolePrompt,
		})
	}
}