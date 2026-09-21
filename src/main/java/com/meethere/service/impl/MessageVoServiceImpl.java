package com.meethere.service.impl;

import com.meethere.dao.MessageDao;
import com.meethere.dao.UserDao;
import com.meethere.entity.Message;
import com.meethere.entity.User;
import com.meethere.entity.vo.MessageVo;
import com.meethere.service.MessageVoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class MessageVoServiceImpl implements MessageVoService {
    @Autowired
    private MessageDao messageDao;
    @Autowired
    private UserDao userDao;

    @Override
    public MessageVo returnMessageVoByMessageID(int messageID) {
        Message message=messageDao.findByMessageID(messageID);
        if (message == null) {
            return null;
        }

        User user=userDao.findByUserID(message.getUserID());
        String userId = user != null ? user.getUserID() : message.getUserID();
        String userName = user != null ? user.getUserName() : "用户数据缺失";
        String picture = user != null ? user.getPicture() : "";
        MessageVo messageVo=new MessageVo(message.getMessageID(),userId,message.getContent(),message.getTime(),userName,picture,message.getState());

        return messageVo;
    }

    @Override
    public List<MessageVo> returnVo(List<Message> messages) {
        List<MessageVo> list=new ArrayList<>();
        for(int i=0;i<messages.size();i++){
            MessageVo messageVo = returnMessageVoByMessageID(messages.get(i).getMessageID());
            if (messageVo != null) {
                list.add(messageVo);
            }
        }
        return list;
    }
}
