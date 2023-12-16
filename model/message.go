package model

import "time"

type Message struct {
	Phone string
	Role string
	BotRole string
	Time time.Time
	Content string
}

func (message *Message) AddMessage() {
	DB.Create(&message)
}

func (message *Message) GetNewestMessage(n int) {
	DB.Order("time").Offset(n).Where("phone = ?", message.Phone).Find(&message)
} 