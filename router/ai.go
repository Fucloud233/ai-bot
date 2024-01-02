package router

import (
	"ai-bot/service"

	"github.com/gin-gonic/gin"
)

func Router() *gin.Engine {
	gin.SetMode(gin.DebugMode)

	r := gin.Default()
	r.POST("index/login", service.Login)
	r.POST("login", service.UserLogin)
	r.POST("register", service.CreateUser)

	/* Notice: we don't need this backend to send and get messages not 
	 * these functions are moved to python-backend */
	// r.POST("messages", service.PostMessages)
	// r.POST("message", service.PostMessage)
	// r.GET("messages", service.GetNewestMessage)
	// r.DELETE("message/all", service.DeleteAllMessages)

	r.PUT("role/prompt", service.UpdateRolePrompt)
	r.GET("role/prompt", service.GetRolePrompt)

	return r
}
