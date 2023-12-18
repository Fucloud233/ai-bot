package router

import (
	"ai-bot/service"

	"github.com/gin-gonic/gin"
)

func Router() *gin.Engine {
	gin.SetMode(gin.DebugMode)

	r := gin.Default()
	r.POST("index/login", service.Login)
	r.POST("register", service.CreateUser)

	r.POST("messages", service.PostMessages)
	// https://www.flysnow.org/2019/12/13/golang-gin-parameters-in-path
	r.GET("messages", service.GetNewestMessage)

	return r
}
