--视频播放排名
select video_id,count(name) as total,name,created_at from tb_video_report where created_at > '2019-09-19 17:30' and created_at < '2019-09-21 17:31' and video_id>0 group by name having total>1 order by total desc;

--订单统计
select mac,out_trade_no,add_time,FROM_UNIXTIME(add_time,'%Y-%m-%d %H:%i:%S'),status from tb_orders where out_trade_no > '201909271731' and out_trade_no < '201909281731' order by id desc;

--新增MAC记录
select * from tb_member_uuid where created_at > '2019-09-21 17:30' and created_at < '2019-09-22 17:31' order by created_at asc;

--新增会员
select * from tb_members  where created_at < '2019-09-22 17:31' order by created_at desc;


--绑定MAC记录
select * from tb_member_mac where created_at < '2019-09-22 17:31' and created_at > '2019-09-21 17:30';

--视频播放与课程
select t.name_remark as grade, t.name as point_name,v.name,count(v.video_id) as total from tb_course_structure_tree as t 
  inner join tb_course_video_detail as c 
  on t.id =c.foreign_course_structure_tree
  inner join tb_video_report as v on v.video_id = c.id where v.created_at > '2019-09-22 17:31' and v.video_id>0 group by v.name having total >1 order by total desc;
  
--电视启动/活跃用户

--累计用户  
select * from tb_launch_log where created_at > '2019-09-22 17:30' group by mac order by created_at asc;

--当天活跃用户
select * from tb_launch_log where created_at > '2019-09-27 17:30' and  created_at < '2019-09-28 17:30' group by mac order by created_at asc;


--7日留存 11

select * from tb_launch_log where created_at < '2019-09-27 17:30' and created_at > '2019-09-20 17:31' and mac in (
select mac from tb_member_uuid where created_at < '2019-09-20 17:31' and created_at > '2019-09-19 17:31'
) group by mac;


--7日前那一天的用户 --58

select * from tb_launch_log where created_at < '2019-09-28 17:31' and created_at > '2019-09-21 17:31' and mac in (
select mac from tb_member_uuid where created_at < '2019-09-21 17:31' and created_at > '2019-09-20 17:31')
group by mac;


--次日留存 8/39
select * from tb_launch_log where created_at < '2019-09-28 17:31' and created_at > '2019-09-27 17:31' and mac in (
select mac from tb_member_uuid where created_at < '2019-09-27 17:31' and created_at > '2019-09-26 17:31'
);


select * from tb_launch_log where created_at < '2019-09-20 17:31' and created_at > '2019-09-19 17:31' and mac in (
select mac from tb_member_uuid where created_at < '2019-09-19 17:31' and created_at > '2019-09-18 17:31'
);


--历史启动记录
select a.channel,a.mac,a.zone,a.device, (case when a.mac in (
    select  b.mac  from tb_launch_log as b where b.created_at < '2019-09-29 17:31' group by b.mac having count(b.mac)>1 order by count(b.mac) desc
    ) then '是' else '否' end ) as repeat_stat,a.created_at,a.updated_at from tb_launch_log as a
 where a.created_at < '2019-09-29 17:31' order by a.created_at desc;