package com.meethere.service.impl;


import com.meethere.dao.OrderDao;
import com.meethere.dao.VenueDao;
import com.meethere.entity.Order;
import com.meethere.entity.Venue;
import com.meethere.entity.vo.OrderVo;
import com.meethere.service.OrderService;
import com.meethere.service.OrderVoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class OrderVoServiceImpl implements OrderVoService {
    @Autowired
    private OrderDao orderDao;
    @Autowired
    private VenueDao venueDao;


    @Override
    public OrderVo returnOrderVoByOrderID(int orderID) {
        Order order=orderDao.findByOrderID(orderID);
        if (order == null) {
            return null;
        }

        Venue venue=venueDao.findByVenueID(order.getVenueID());
        String venueName = venue != null ? venue.getVenueName() : "场馆数据缺失";
        OrderVo orderVo=new OrderVo(order.getOrderID(),order.getUserID(),order.getVenueID(),venueName,
                                    order.getState(),order.getOrderTime(),order.getStartTime(),order.getHours(),order.getTotal());

        return orderVo;
    }

    @Override
    public List<OrderVo> returnVo(List<Order> list) {
        List<OrderVo> list1=new ArrayList<>();
        for(int i=0;i<list.size();i++) {
            OrderVo orderVo = returnOrderVoByOrderID(list.get(i).getOrderID());
            if (orderVo != null) {
                list1.add(orderVo);
            }
        }
        return list1;
    }
}
