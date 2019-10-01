<?php
    // user 用户
    const USER_STORE = '/moocapi/tvapi/user/store';
    // user 用户
    const USER_SHOW = '/moocapi/tvapi/user/show';
    // user 用户
    const USER_DESTROY = '/moocapi/tvapi/user/destory';
    // user 用户
    const USER_UPDATE = '/moocapi/tvapi/user/update';

    // study 学习,获取菜单
    const STUDY_HEAD_MENU = '/moocapi/tvapi/study/head/menu';

    // 视频相关
    const VIDEO_POINT = '/moocapi/tvapi/ponitvideos';
     // 视频相关
    const VIDEO_THINKTRAIN = 'moocapi/questionvideo/getVideoByExaminationId/{examId}';
     // 视频相关
    const VIDEO_SYNCH = 'moocapi/studycenter/ponitvideos/{examId}';
     // 增加一条播放记录
    const VIDEO_ADD_ITEM = '/moocapi/uservideo';

    // 试卷相关
    const PAPER_LIST = '/moocapi/tvapi/paper/list';

    // 考试相关
    const EXAM_QUESTION = '/moocapi/tvapi/exam/qesution';
     // 考试相关
    const EXAM_ANSWER = '/moocapi/tvapi/exam/answer';
     // 考试相关
    const CHECK_EXAM = '/moocapi/tvapi/exam/submit/info';

    // 能力评估
    const STUDENT_STATISTICS_CAPABILITY_EVALUATION = '/moocapi/studentStatistics/capabilityEvaluation';
    // 能力评估
    const STUDENT_STATISTICS_POINT_RATE = '/moocapi/studentStatistics/pointRateStatistics';
    // 能力评估
    const STUDENT_STATISTICS_POINT_RADAR = '/moocapi/studentStatistics/pointRadarStatistics';

    // 所有单元
    const REPORT_ANALYSIS_SKILL_COUNT = '/api/analysis/skill/count/{userId}/';
    // 学习时间详情
    const REPORT_ANALYSIS_CHART_LINE = '/api/analysis/chart/line/{userId}/{dateType}';
     // 单元详情 --> 各个单元的统计情况
    const REPORT_ANALYSIS_SKILL_EACH_COUNT = '/api/analysis/skill/each/count/{userId}';
    // 某个学习节点下答题统计情况
    const REPORT_ANALYSIS_LIST_ANSWER_MINE = '/api/analysis/list/answer/mine/{skillId}';
    // 学习情况详情
    const REPORT_ANALYSIS_CHART_LINE_SITUATION = '/api/analysis/chart/line/situation/{userId}';
    // 返回总学习时间+学过的知识点+ 未掌握的知识点
    const REPORT_ANALYSIS_BASE_SITUATION = '/api/analysis/base/situation/{userId}/space/{spaceId}';

    // 单题提交答案
    const MOBILE_SUB_ANSWER_SINGLE='/moocapi/answer/submitAnswer' ;
    // 提交答案临时接口（整卷或单卷使用，非最后一道习题提交这个接口）
    const MOBILE_SUB_TEMP_ANSWER='/moocapi/answer/temporary' ;
    // 提交答案最后一题接口（整卷使用，最后一道习题提交这个接口）
    const MOBILE_SUB_ANSWER_FULL_PAPER='/moocapi/answer/assignment' ;
    // 重新做题接口
    const MOBILE_RESET_ANSWER='/moocapi/answer/resetAnswer' ;


    // 添加收藏到收藏列表
    const FAVORITE_ADD_FAVORITE_RECORD = '/moocapi/favorite/addFavoriteRecord?questionId={questionId}&examinationId={examinationId}&answerRecordId={answerRecordId}';
    // 获取 试卷名列表
    const FAVORITE_EXAMINATION_LIST = '/moocapi/favorite/examinationlist';
    // 获取收藏列表
    const FAVORITE_LIST = '/moocapi/favorite/list';
    // 移除收藏列表
    const FAVORITE_REMOVE_FAVORITE_RECORD = '/moocapi/favorite/removeFavoriteRecord';


    // 获取申诉列表
    const STUDY_RECORD_APPEAL_LIST = '/moocapi/studyrecord/appeallist';
    //班级排名
    const STUDY_RECORD_CLASS_ROOMS_USER_STUDY_RECORD_COUNT = '/moocapi/studyrecord/classRooms/{classRoomId}/userStudyRecordCount';
    // 获取 试卷名列表(筛选条件之一)
    const STUDY_RECORD_EXAMINATION_LIST = '/moocapi/studyrecord/examinationlist';
    // 获取 答题记录列表
    const STUDY_RECORD_LIST = '/moocapi/studyrecord/list';
    // 获取 错题集 列表
    const STUDY_RECORD_WRONG_LIST = '/moocapi/studyrecord/wronglist';

        // 1.检查学生学习状态
    const SELF_LEARN_EVALUATE='/tvapi/check/evaluate/spaceId/{spaceId}/userId/{userId}' ;
        // 2.初始化评估数据
    const SELF_LEARN_RE_EVALUATE='/tvapi/userId/{userId}/spaceId/{spaceId}/init/{reEvaluate}?clearMaster={clearMaster}' ;
        // 3.习题请求接口
    const SELF_LEARN_QUESTION='/tvapi/question/list?questionIds={questionIds}' ;
        // 4.获取下一道题Id
    const SELF_LEARN_NEXT_QUESTION_ID='/tvapi/userId/{userId}/spaceId/{spaceId}/skillId/{skillId}/pass/{pass}/result' ;
        // 5.提交习题答案
    const SELF_LEARN_SUBMIT_ANSWER='/tvapi/submitAnswer' ;
        // 6.获取下一个微技能Id
    const SELF_LEARN_NEXT_SKILL_ID='/tvapi/push/topic/spaceId/{spaceId}/userId/{userId}/reEvaluate/{reEvaluate}/skill' ;
        // 7.根据微技能ID获取下一道题Id
    const SELF_LEARN_NEXT_QUESTION_ID_BY_SKILLID='/tvapi/push/topic/skillId/{skillId}/userId/{userId}/question?answerType={answerType}&spaceId={spaceId}' ;
    // 8.检获取学生详情信息
    const SELF_LEARN_STUDENT_DETAIL='/moocapi/tvapi/user/show' ;
    // 9.学生答题正确后，更新学生状态，
    const SELF_LEARN_STUDENT_UPDATE_STATUS='/tvapi/update/study/status/spaceId/{spaceId}/userId/{userId}/groupId/{groupId}/skillId/{skillId}?currentSkillId={currentSkillId}' ;

    //1.获取单元学习头菜单
    const SELF_LEARN_SECTION_MENUE='/tvapi/section/{skillId}/list' ;
    //2.单元学习模块盘【评估阶段】接口，可以获取下一道题
    const SELF_LEARN_SECTION_EVALUATE='/tvapi/section/userId/{userId}/spaceId/{spaceId}/init/{reevaluate}' ;
    //3.单元学习模块【学习阶段】获取下一道题ID
    const SELF_LEARN_SECTION_LEARN_NEXT_QUESTION_ID='/tvapi/section/userId/{userId}/spaceId/{spaceId}/skillId/{skillId}/pass/{pass}/result' ;
    //4.获取当前微技能的路径导航信息
    const SELF_LEARN_CUR_SKILL_PATH_INFO='/api/answer/breadcrumb/skillId/{skillId}/list' ;
    //5.单元学习模块【评估阶段】获取下一道题ID，其中参数 answerType 有三个可选值： evaluate、learn、preview
    const SELF_LEARN_SECTION_EVALUATE_NEXT_QUESTION_ID='/tvapi/push/topic/skillId/{skillId}/userId/{userId}/question?answerType={answerType}&spaceId={spaceId}' ;
    //6.获取当前微技能对应的视频列表
    const SELF_LEARN_SECTION_VIDEO_LIST='/api/learn/videos/skillId/{skillId}' ;
    //7.单元学习模块盘【评估阶段】接口，可以获取下一道题
    const SELF_LEARN_SECTION_NEXT_SKILLID='/tvapi/section/push/topic/spaceId/{spaceId}/userId/{userId}/reEvaluate/{reEvaluate}/skill' ;

    //1.单元学习模块【预习阶段】获取下一道题ID
    const SELF_LEARN_PREVIEW_NEXT_QUESTION_ID='/tvapi/push/topic/skillId/{skillId}/userId/{userId}/preview/question?currentChapterId={currentChapterId}' ;
    //1.单元学习模块【预习阶段】获取预习相关的视频列表
    const SELF_LEARN_PREVIEW_VIDEO_LIST='/tvapi/videos/chapterId/{chapterId}' ;

    //自适应学习之【报表相关】
    //1.获取掌握的知识点详情（对应PRD右侧数据）
    const SELF_LEARN_REPORT_RIGHT='/tvapi/skill/count/{userId}/spaceId/{spaceId}' ;
    //2.关联上一个接口的serialNumber，将相关serialNumber转换为中文
    const SELF_LEARN_REPORT_RIGHT_TEXT='/api/evaluate/userId/{userId}/spaceId/{spaceId}/result/init';
    //3.学习路线图【已经掌握的、未掌握的、推荐学习路径】
    const SELF_LEARN_REPORT_LEFT='/api/analysis/skill/{userId}/learn-path?spaceId={spaceId}&maxSize=100';
