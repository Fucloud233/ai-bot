package model

import "time"

const (
	User string = "user"
	Assistant string = "assistant"
)

type Message struct {
	Id int `json:"-" gorm:"primary;AUTO_INCREMENT"`
	Phone string `json:"-" `
	BotRole string `json:"-"`
	Time time.Time `json:"time"`
	SimpleMessage
}

type SimpleMessage struct {
	Role string `json:"role"`
	Content string `json:"content"`
}

func NewMessage(phone string, botRole string, role string, content string, time time.Time) Message {
	var message Message
	message.Phone = phone
	message.BotRole = botRole
	message.Role = role
	message.Content = content
	message.Time = time
	return message
}

func NewSimpleMessage(role string, content string) SimpleMessage {
	return SimpleMessage {
		Role: role,
		Content: content,
	}
}

func (msg *Message) ToSimpleMessage() SimpleMessage {
	return NewSimpleMessage(msg.Role, msg.Content)
}

func AddMessages(messages *[]Message) error {
	return DB.Create(&messages).Error
}

func GetNewestMessage(phone string, number int, offset int, duration int) ([]Message, error) {
	var message []Message

	// get messages in N minutes
	err := DB.Select([]string{
		"*", "TIMESTAMPDIFF(MINUTE, time, NOW()) as diff",
	}).Where("phone = ?", phone).Order("id desc").Limit(number).Offset(offset).Having("diff < ?", duration).Find(&message).Error

	// reserve array
	for i, j := 0, len(message)-1; i < j; i, j = i+1, j-1 {
		message[i], message[j] = message[j], message[i]
	}
	return message, err
} 

func GetMessages(phone string, number int, offset int ) ([]Message, error) {
	var message []Message
	err := DB.Order("id desc").Limit(number).Offset(offset).Where("phone = ?", phone).Find(&message).Error
	
	// reserve array
	for i, j := 0, len(message)-1; i < j; i, j = i+1, j-1 {
		message[i], message[j] = message[j], message[i]
	}
	return message, err
} 

func DeleteAllMessages(phone string, botRole string) error {
	var message Message
	return DB.Where("phone = ? and bot_role = ?", phone, botRole).Delete(&message).Error
}