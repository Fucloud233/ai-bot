package service

import (
	"ai-bot/model"
	"ai-bot/utils/error"
	"net/http"

	"github.com/gin-gonic/gin"
)

// func CreateUser(c *gin.Context) {
// 	user := model.UserBasic{}
// 	user.Phone = c.Query("phone")
// 	user.Password = c.Query("password")
// 	err := model.CreateUser(&user)
// 	if err != nil {
// 		c.JSON(http.StatusInternalServerError, gin.H{})
// 	} else {
// 		c.JSON(http.StatusOK, gin.H{})
// 	}
// }

func CreateUser(c *gin.Context) {
	var user model.UserBasic
	err := c.ShouldBindJSON(&user)

	if err != nil {
		c.JSON(http.StatusBadRequest, error.GetErrorMessage(error.JSONParseError))
		return
	}

	if model.CheckUserExist(user.Phone) {
		c.JSON(http.StatusBadRequest, error.GetErrorMessage(error.UserExist))
		return
	}

	err1 := model.CreateUser(&user)
	err2 := model.InitRoles(user.Phone)

	status := http.StatusOK
	if err1 != nil && err2 != nil {
		status = http.StatusInternalServerError
	}

	c.JSON(status, "")
}

func Login(c *gin.Context) {
	user := model.UserBasic{}
	phone := c.PostForm("phone")
	password := c.PostForm("phone")
	findUser := model.FindUserByPhone(phone)
	if findUser.Phone != "" {
		if password == findUser.Password {
			c.JSON(http.StatusOK, gin.H{})
		} else {
			c.JSON(http.StatusOK, gin.H{
				"message": "密码错误",
			})
			return
		}
	} else {
		user.Phone = phone
		user.Password = password
		err := model.CreateUser(&user)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{})
		} else {
			c.JSON(http.StatusOK, gin.H{})
		}
	}
}


func UserLogin(c *gin.Context) {
	var user model.UserBasic
	err := c.ShouldBindJSON(&user)

	if err != nil {
		c.JSON(http.StatusBadRequest, error.GetErrorMessage(error.JSONParseError))
		return
	}

	findUser := model.FindUserByPhone(user.Phone)
	if findUser.Phone == "" {
		c.JSON(http.StatusNotFound, "")
	} else if user.Password != findUser.Password {
		c.JSON(http.StatusForbidden, "")
	} else {
		findUser.Password = ""

		c.JSON(http.StatusOK, gin.H{
			"info": findUser,
		})
	}
}