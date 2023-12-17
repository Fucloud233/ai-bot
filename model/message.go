package model

import "time"

type Message struct {
	Phone string `json: "phone" binding: "-"`
	Role string `json: "role"`
	BotRole string `json: "bot_role" binding: "-"`
	Time time.Time `json: "time"`
	Content string `json: "content"`
}

func AddMessages(messages *[]Message) error {
	return DB.Create(&messages).Error
}

func (message *Message) GetNewestMessage(n int) {
	DB.Order("time").Offset(n).Where("phone = ?", message.Phone).Find(&message)
} 