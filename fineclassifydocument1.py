# -*- coding: UTF-8 -*-

from imagePretreatmentGuang import *
from ocr import *
import utils
import numpy
from PIL import *
import re
import roughclassification
from time import *


def fineClassifyDocument(imageFile, type):
    orignImageFile = imageFile.copy()
    count = 0
    lineNum = 0
    image = numpy.array(orignImageFile)
    orignHeight = len(image)
    orignWidth = len(image[0])
    orignImageFile = orignImageFile.crop((int(0.1 * orignWidth), int(0.05 * orignHeight), int(0.8 * orignWidth), int(0.85 * orignHeight)))
    # orignImageFile.show()
    image = numpy.array(orignImageFile)
    orignHeight = len(image)
    orignWidth = len(image[0])
    orignImageFile = orignImageFile.convert('1')
    imageFile = orignImageFile.copy()
    # imageFile.show()
    imageFile = imageFile.resize((orignWidth/10, orignHeight/10), Image.BILINEAR)
    # imageFile.show()
    image = imageFile.load()
    (width, height) = imageFile.size
    lineHeight = float(3)
    total = height * width
    for i in xrange(height):
        for j in xrange(width):
            if image[j, i] > 250:
                count = count + 1
    if float(count) / float(total) < 0.01:
        return 'blank'
    row = utils.tohisto(imageFile, 'row')
    # ce shi
    for y in xrange(height):
        up = 0
        down = 0
        for i in xrange(y, height):
            if row[i] > 1:
                y = i + 1
                up = i - 1 if i - 1 > 0 else 0
                break
            if i == height - 1:
                y = height
        for i in xrange(y, height - 2):
            if (row[i] <= 1) & (row[i + 1] <= 1) & (row[i + 2] <= 1):
                y = i
                down = height - 1 if i + 1 > height - 1 else i + 1
                break
            if i == height - 1:
                y = height
        if float(lineHeight) < float(down - up) < float(height * 0.35):
            # lineImageNew = imageFile.crop((0, up, width, down))
            # lineImageNew.show()
            lineImage = orignImageFile.crop((0, int(up * 10), int(orignWidth), int(down * 10)))
            if bool(lineImage) == False:
                continue
            lineNum = lineNum + 1
            txt = Ocr(lineImage, type)
            if txt == '﻿':
                lineImage = utils.repair(lineImage)
                txt = Ocr(lineImage, type)
            # lineImage.show()
            txt = txt.replace('\t', '').replace('\n', '').replace('\t\n', '')
            txt = txt.decode('utf-8')
            image = imageFile
            if re.match(u'.*[仲伸]裁委[员贝].{1,3}|.?法律文书生效证明.?', txt):
                num = 0
                for y2 in range(down + 1, height):
                    for i in range(y, height):
                        if row[i] > 1:
                            y2 = i + 1
                            up = i - 1 if i - 1 > 0 else 0
                            break
                    for i in range(y2, height - 1):
                        if row[i] < 1:
                            down = height - 1 if i + 1 > height - 1 else i + 1
                            y2 = i + 1
                            break
                    if float(height * 0.35) > float(down - up) > float(lineHeight):
                        lineImage = orignImageFile.crop((0, int(up * 10), int(orignWidth), int(down * 10)))
                        if bool(lineImage):
                            num = num + 1
                            txt = Ocr(lineImage, type)
                            if txt | re.match(txt, '\\w'):
                                txt = Ocr(lineImage, type)
                            if re.match(u".{0,2}[裁截]决书|.{0,1}仲[裁栽]{1,2}决书.?", txt):
                                if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                                    return '执行依据和生效证明'
                                return '执行依据和生效证明Front'  # 是否连页，最后处理
                            if num > 2:
                                break
            if re.match(u'.*律师事务所公函|.{2,5}援助公函', txt):
                return '授权委托书、身份证明'
            if re.match(u'.*公函', txt):
                result = contentEndCheck(image, row, imageFile)
                if result == '授权委托书、身份证明':
                    return '授权委托书、身份证明'
            else:
                if re.match(u'申请书', txt):
                    # 不知道是什么
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        result = contentEndCheck(image, row, lineImage)
                        if result == '停止执行':
                            return '停止执行'
                        if result == '授权委托书、身份证明':
                            return '授权委托书、身份证明'
                        return 'execution'
                    return 'executionFront'
                if re.match(u'.{0,2}撤销.{2,6}|.{0,2}[攒撤撒]诉.*|.{0,3}[拆诉]申请.{0,3}|.?撤案申请.?', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '撤诉书'
                    return '撤诉书Front'
                if re.match(u'.{2,4}司法局回复函|.*社会调[杳查]表', txt):
                    return '缓刑适用社会调查表'
                if re.match(u'.{0,3}评估意.{0,3}|.{2,4}调[杳查]报告|.{3,7}风.{1,3}估报告|.{0,3}评.{1,3}见.{0,2}', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '缓刑适用社会调查表'
                    return '缓刑适用社会调查表Front'
                if re.match(u'.*调.{0,3}笔.{0,3}录.{0,3}', txt):
                    return '和解协议'
                elif re.match(u'.*授.{0,2}[权杈].{0,3}[托抚].?书.{0,4}|.{0,5}委.{1,3}|委[托抚拄]书编号.{2,7}.{0,5}身[纷份]证'
                              u'[明朋].{0,3}|.{0,2}公.{1,5}.{1,4}[\d]{7,}.*|.*律.{2,5}所[^信]?函.{0,6}|法人身[纷份]证.*|.*'
                              u'代码信息.*.*执业证类别.*|.*有限公司注册.*一社会信用.*[\d]{6,}|.{0,3}[法定代表人身[纷份]证复印件]{5,'
                              u'}.{0,4}|.*出庭函|.{0,2}业[机矶][构枸恂].*|执业证.*|.{0,4}居民户口簿.*|.?推荐信.?|[授投]权书|.{0,8'
                              u'}法人证书|.*度.{0,3}核备.*|.{0,3}注册号[\d]{7,18}.{0,3}|.{0,3}登记项目|.?组织.构代码证.*|律.{2,5'
                              u'}所[^信]?函.{0,5}第.{1,6}号|.{2,8}律师事务所|营.[执捌]照|.*统一社会信用代.*|亍聿师事.{1,4}所函|.'
                              u'{0,6}律师事.{1,3}函|.{0,6}律师事务.{0,4}|授[权衩杈]委.{2,6}|.{0,4}身[份伯]证明.?|.*一[社祉]会信用代'
                              u'.*|.{1,3}身.?号码[\d]{7,}|.明|法人(代表)?.?[证正]明.{0,6}|.?授.{1,3}|律师.?务所名称.{2,9}|法律工作者证'
                              u'|组织机构代码证|.*[统脘]一[社仕]会信用代码.*|推荐信|法律服务所.{0,3}|.?委托书编号.?', txt):
                    return '授权委托书、身份证明'
                if re.match(u'[悔梅]过书', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '悔过书'
                    return '悔过书Front'
                if re.match(u'.*公[诉拆].?见书', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '公诉词'
                    return '公诉词Front'
                if re.match(u'.{0,8}[辨辩]护.{1,7}|[辨辩].[词询]|.*辩护词', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '辩护词'
                    return '辩护词Front'
                if re.match(u'.{0,6}[代筏].?词.?|.*代理意见.{0,3}|.*代[王壬][里理]词.?|.*代[王壬]里意见.{0,3}|.?分割意见.?', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '代理词'
                    return '代理词Front'
                if re.match(u'.{0,7}[冉再][审窜].{0,4}|.{0,8}申诉.{1,3}', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '再审'
                    return '再审Front'
                if re.match(u'.{0,5}诉讼代理人推荐函.{0,4}', txt):
                    return '诉讼代理人推荐函'
                if re.match(u'.{2,5}上诉.{0,2}|.{0,6}抗诉.{0,6}|.{0,3}上诉状.{0,5}|行.?上.?状|行政.?诉状.{0,6}|.{2,6}'
                            u'上诉.{0,1}状', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '抗诉书、上诉书'
                    return '抗诉书、上诉书Front'
                if re.match(u'[^送达]{0,8}[诉讲拆][状书].{0,5}|.*加.{0,2}讼.{0,10}|.*诉讼申.*|.{0,6}再.申请[书]{0,1}自诉状'
                            u'|.?自述材料.?|.{0,3}附带民事诉.?|.?送达.{0,2}起[诉讲讶拆].{0,3}|[起赳].书|.?变更诉讼请求申请书.?'
                            u'|.?变更起诉决定书.?|.?诉讼请求申请.?', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '起诉书'
                    return '起诉书Front'
                if re.match(u'.{0,7}和解协议[书]?|.{0,3}谅.?书|.{0,7}[禾口|和]解申请[书]?', txt):
                    return '刑事附带民事部分调解书'
                if re.match(u'.{0,3}[和调]解.{2,3}|调.{0,2}申请书|.{2,6}议书|.{0,2}[谅凉][解牌].{0,2}|.?民事赔偿协议书.?', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '和解协议'
                    return '和解协议Front'
                if re.match(u'.?执行通知书.{0,5}|.{3,8}发还裁决款审批表.?|.{0,5}收.?条', txt):
                    return '执行通知书存根和回执（释放证回执）'
                if re.match(u'.*保全申请书.?|.*账户信息.?|.{0,3}矫正告知书.?|.{0,4}矫正人员.{2,5}通知单|.?接受社区[矫娇]正保证书.?', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '执行通知书存根和回执（释放证回执）'
                    return '执行通知书存根和回执（释放证回执）Front'
                if re.match(u'.{0,8}判[决泱]书.?|.{0,3}裁.{0,3}定.{0,3}|.?裁定书原稿.?|.{0,8}民事调.{0,4}书.?|.{0,8}民事裁定.{0,2}书.*'
                            u'|.{0,8}民.?判[决泱].{0,2}书.?|民.?判[决泱].?', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '判决书'
                    return '判决书Front'
                if re.match(u'.*执行工作日志.?', txt):
                    return '执行工作日志'
                if re.match(u'.{0,3}复议申请书.*|.{0,6}异议申请书.?|执行异议书.{0,4}|.*行.{0,3}申请书.{0,2}|申请{0,1}.?执行书.{0,6}'
                            u'|.{0,2}强制执行.*', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '申请执行书'
                    return '申请执行书Front'
                if re.match(u'.{0,1}附.{0,1}', txt):
                    return '尾页'
                if re.match(u'^.{0,2}换[押砷].*|.{0,4}[提捉]讯.{0,5}|换.证.?^拘传票|.?换[押砷]票.?|[提捉][押砷]票.?', txt):
                    return '换押票'
                if re.match(u'.?证人出庭作证申请书.{0,4}', txt):
                    return '证人出庭申请书'
                if re.match(u'.问.录|.?询问笔录.?', txt):
                    if fileEndCheck(image, row, 0.06) | endCheck(image, row, lineImage):
                        return '讯问笔录、审问笔录、询问笔录'
                    return '讯问笔录、审问笔录、询问笔录Front'
                if re.match(u'.?委托执行函.{0,4}', txt):
                    return '委托执行函'
                if re.match(u'.{0,5}证据光盘目录.*|调.{0,3}证据申请书', txt):
                    return '申请调取证据材料'
                if re.match(u'证.?[据居].{0,4}|案件目录|.?受案登记表.?|.?受案回执.?|鉴定意见书|质证.{0,2}录|.*气象证[明朋].*'
                            u'|.*被罚.*|.*罚款处.*|.{0,4}鉴定书.{0,3}|.*损车牌.*|房屋登记.{0,2}|征收.{0,4}清单.?|延期举证申请书'
                            u'|婚姻登记记录.{0,4}|一、居.?户口.?具.*|.?常住.{0,4}记卡.{0,4}|注意事项|.{2,8}列表|.{0,3}调[杳查]笔录.{0,7}'
                            u'|情况说[明阴]|.{0,1}情况说日月.{0,2}', txt):
                    return '证据'
                if re.match(u'领款审批表.{0,4}', txt):
                    return '查询、冻结、扣划裁定书、协助执行通知书等财产调查和控制手续及回执'
                if re.match(u'.{0,2}案申[清请]', txt):
                    return '撤回执行申请书'
                if re.match(u'.?执行笔录.?', txt):
                    if fileEndCheck(image, row, 0.2) | endCheck(image, row, lineImage):
                        return '向申请人了解执行线索笔录和向被执行人执行笔录'
                    return '向申请人了解执行线索笔录和向被执行人执行笔录Front'
                if re.match(u'.{0,5}出.?法庭通知书.{0,2}|申请证人出庭作证申请书', txt):
                    return '公诉人、辩护人出庭通知书'
                if re.match(u'.{0,3}延期审理.{0,5}', txt):
                    return '延长审限的决定、报告及批复'
                if re.match(u'.*讼费收.{0,2}|.*诉讼费专用票据.*|.?减.{0,2}交.*纳.*诉.*讼.?申请书.?|.?减.?免.?缓.?审批表.?|.*收[入人].?般缴款书.*'
                            u'|.?[瑗缓].?减.?[兔免]诉讼.{0,1}审批表.?', txt):
                    return '缴纳诉讼费'
                if re.match(u'邮件号码.*|.*投递并签收.*|.*邮.{1,2}号码:.*|运单.程|.*揽投员.*|.*[送达]达.{0,3}|.*EMS.*" + "'
                            u'|.{0,6}网上寄件.?|.*送达.*送达.*|.?送达公告.?|.?送达案件登记表.?|.?送达回证.?|受送达[人入].*', txt):
                    return '送达回证'
                if re.match(u'.?保证书.?|.*担保书|.?法庭笔录.?|.?庭审笔录.?|.?法庭审[理埋]笔录.?|.*审判笔录|.?开庭笔录.?|.?法庭审[王壬]里笔录.?'
                            u'|.?是否公开.?公开审理|.?是否公开.?不公开审理', txt):
                    if fileEndCheck(image, row, 0.2) | endCheck(image, row, lineImage):
                        return '保证书、担保书'
                    return '保证书、担保书Front'
                if re.match(u'.?庭前会议笔录.?|.?证据交换笔录.?', txt):
                    if fileEndCheck(image, row, 0.2) | endCheck(image, row, lineImage):
                        return '庭前会议笔录'
                    return '庭前会议笔录Front'
                if re.match(u'.?庭前工作笔录.?|.?庭前.?准.?备.?工作记录.?', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '庭前工作笔录'
                    return '庭前工作笔录Front'
                if re.match(u'.?传[票禀].{0,8}', txt):
                    return '提审、询问当事人、提押票、传票'
                if re.match(u'.*证据.*交换.*笔录.*', txt):
                    return '证据交换笔录'
                if re.match(u'.{1,7}案件.{1,7}流.*管理.{1,3}|.*立案登记表.{1,6}|.?立案审批表.?|.*案件.*审判流.*|.*立案.*理.*息'
                            u'|.*案件.*立案.*审.*|.?执行案件流程管理情况.?|.*流程.*信息表|.{1,3}审.*案件立案', txt):
                    return '案件流程信息表'
                if re.match(u'.?改变管辖通知书.{1,7}|.*指定管辖决定书.*', txt):
                    return '改变管辖通知书'
                if re.match(u'.{0,8}[立案|应诉|应拆|诉讼].?知书.{0,5}|.*补充材料通知书.{0,5}', txt):
                    return '立案受理通知书'
                if re.match(u'.*阅卷.*知书.*', txt):
                    return '阅卷通知书'
                if re.match(u'.*法院适用简易程序.*', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '简易程序适用'
                    return '简易程序适用Front'
                if re.match(u'.*送达起诉书.{0,2}笔录', txt):
                    return '送达起诉书笔录'
                if re.match(u'.{0,2}司法公.{0,2}知书.?', txt):
                    return '司法公开告知书首页'
                if re.match(u'.{0,3}监督.{0,2}|.*廉政监督卡|.*诉讼[冈风凤]险.{0,5}', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '司法公开告知书'
                    return '司法公开告知书Front'
                if re.match(u'.*保证书.{5,11}|.{1,3}保.{0,3}候审.{1,3}通知书.{1,6}|.{0,2}居住.{0,2}通知书.{1,6}|'
                            u'.{1,3}保.{0,3}候审.{1,3}决定书.{1,6}" + "|执行.{0,2}通知书.{0,5}', txt):
                    return '变更强制措施决定及对家属通知书'
                if re.match(u'.?查封.{3,7}财产.{1,7}|.?查询存款函.{1,6}|诉讼保全.{0,3}', txt):
                    return '诉讼保全裁定书、搜查、勘验、查封笔录及查封、扣押物品清单'
                if re.match(u'.?准许调[取查].{0,3}[书令].{0,4}', txt):
                    return '当事人、律师调取证据申请、准许调取证据令及调取的证据材料'
                if re.match(u'.*鉴定结论|.{0,4}鉴定委托书.{4,10}|.{0,2}笔录.{7}', txt):
                    return '赃、证物委托鉴定书及鉴定结论'
                if re.match(u'.?被告人坦白.{0,5}问题登记表.?|.?查证材料.?', txt):
                    return '被告人坦白交代、揭发问题登记表及查证材料'
                if re.match(u'.?限制出境决定书.{7}', txt):
                    return '限制出境决定书	'
                if re.match(u'.{0,2}申请回避.{1,3}决定书.{7}', txt):
                    return '申请回避及处理决定'
                if re.match(u'[出开]庭通知书.{7}|.{1,4}员出.?法庭通知书|.*告知书|.*合议庭.*成.*员.*通知书.*', txt):
                    return '开庭通知'
                if re.match(u'.*公[告古].{0,8}', txt):
                    return '开庭公告底稿'
                if re.match(u'.*刑建议书.*', txt):
                    return '量刑建议书'
                if re.match(u'.{2}决定书.{7}', txt):
                    return '妨害刑事诉讼拘留罚款决定'
                if re.match(u'.?刑事裁定书.*准许.{0,5}|.*刑[辜事]判决书.*|.*刑事附带民事.{1,3}', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '裁判文书正本'
                    return '裁判文书正本Front'
                if re.match(u'.{0,2}宣判笔录.{0,3}|.判笔.{2,6}|.?判后释法笔录.?|.?委托宣判函.{0,4}	', txt):
                    if fileEndCheck(image, row, 0.2) | endCheck(image, row, lineImage):
                        return '宣判笔录、判后释法笔录首页'
                    return '宣判笔录、判后释法笔录首页Front'
                if re.match(u'.*司法建议书.{2,7}', txt):
                    if fileEndCheck(image, row, 0.2) | endCheck(image, row, lineImage):
                        return '司法建议书'
                    return '司法建议书Front'
                if re.match(u'报送上.*抗.{0,4}件.{2,6}|.{0,2}上诉案件移送函.{0,2}|.{0,2}案件上诉移送函.{0,2}|.?案件移送函.?'
                            u'|.?报送上.?抗.?.?案件.?|.?报送上诉案件函{0,1}.?|.?上诉移送函.?', txt):
                    return '上抗诉案件移送函（稿）'
                if re.match(u'.*退.*卷.*函.*|.?卷函.?', txt):
                    return '退卷函'
                if re.match(u'.{1,3}执行死刑命令.{0,4}死刑.{1,3}', txt):
                    return '执行死刑命令'
                if re.match(u'.*暂停执行死刑的报告及批复.', txt):
                    return '暂停执行死刑的报告及批复'
                if re.match(u'.*验明正身笔录.{0,2}死刑用.{0,2}', txt):
                    return '死刑执行前验明正身笔录'
                if re.match(u'.*执行死刑笔录.{0,2}刑事.{0,3}', txt):
                    return '执行死刑笔录'
                if re.match(u'.?执行死刑报告.?', txt):
                    return '执行死刑报告'
                if re.match(u'.?死刑罪犯照片.?', txt):
                    return '死刑执行前后照片'
                if re.match(u'.*领取骨灰通知书.{3,9}', txt):
                    return '死刑犯家属领取骨灰或尸体通知'
                if re.match(u'.?尸体处理登记表.?', txt):
                    return '尸体处理登记表'
                if re.match(u'.?执行通知书.{3,10}用.?|减刑执行通知书.*用.?" + "|释放通知书.{3,10}用.?|假释执行通知书.*用.?', txt):
                    return '执行通知书'
                if re.match(u'.?发还财物品清单.{1,6}', txt):
                    return '赃物、证物移送清单及处理手续材料'
                if re.match(u'.*减刑.*假.*定书', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '减刑、假释裁定书'
                    return '减刑、假释裁定书Front'
                if re.match(u'.?备考表.?', txt):
                    return '备考表'
                if re.match(u'.?卷内目录.?', txt):
                    return '卷内目录'
                if re.match(u'.*送达.*地址.*书.{0,6}|.*当事.*确认书.{0,6}', txt):
                    return '举证通知书、送达地址确认书和电子送达确认书'
                if re.match(u'.*举证通知书.*|.*电子送达确认书.*', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '举证通知书、送达地址确认书和电子送达确认书'
                    return '举证通知书、送达地址确认书和电子送达确认书Front'
                if re.match(u'诉讼保全.{0,2}书.{0,2}|.*鉴定委托书.*|.*鉴定结论.*|.*通知书.{2,5}重新.{1,3}申请.{0,2}', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '诉讼保全担保书、诉讼保全裁定书正本、鉴定委托书、鉴定结论'
                    return '诉讼保全担保书、诉讼保全裁定书正本、鉴定委托书、鉴定结论Front'
                if re.match(u'.*通知书.{2,5}延长.{2,4}申请.{0,2}|.*通知书.*当事人.*第三人.*|.*通知书.{3,9}举证期限.{0,3}', txt):
                    return '变更举证期限通知书'
                if re.match(u'申请.*程序.{2,4}|.?转换程序通知书.?|民事.{1,6}程序.{1,3}程序.{1,2}', txt):
                    return '变更普通程序审批表'
                if re.match(u'.*证物处理手续.{1,3}', txt):
                    return '证物处理手续'
                if re.match(u'.*受.?[里理]通知书.?|.?驳回申诉.?|.?受.{0,2}案件通知书.?', txt):
                    return '受理案件通知书'
                if re.match(u'.*[不上准].*裁定书', txt):
                    if fileEndCheck(image, row, 0.25) | endCheck(image, row, lineImage):
                        return '执行裁定'
                    return '执行裁定Front'
                if re.match(u'.*财产.*线索.*报告|.{1,4}财产刑执行信息表.?', txt):
                    return '财产线索和报告'
                if re.match(u'.*执行.*进.*知书', txt):
                    return '执行进程告知书'
                if re.match(u'.?由法院.*有关财产.{4,8}|.{1,3}拍卖措施.{1,3}|.*成交确认.{0,4}|.*变卖措施.{1,4}|.*以物抵债.{1,5}'
                            u'|.?鉴定委托书.?|.?价格评估委托书.?|.?拍卖.{0,3}卖.*委托书|.?拍卖通知书.?|.?查封公告.?|查封.{4,8}财产清单'
                            u'|.?拍卖公告.?|.*迁出房屋.{0,2}退出土地.{0,3}|.?搜查令.?|.{0,3}交出财物.{0,6}'
                            u'|.{1,5}生效法律.{1,4}行为.{0,6}" + "|折价赔偿.*财产.{1,5}|代为完成.*|.{1,3}追回财物.{1,6}', txt):
                    return '评估、拍卖等财产变现手续'
                if re.match(u'.{0,7}执行争议.*|.*利害关系.*|案外人.*|复议执行.{1,4}|.?督促执行令.?|.*下级法院.*|.*暂缓执行.*'
                            u'|.*非诉法律文书.*|.*执行裁定.*', txt):
                    return '处理执行争议书'
                if re.match(u'.?执行款过户手续.{2}|领款审批表.?', txt):
                    return '执行款过户手续'
                if re.match(u'.*执行回转.*', txt):
                    return '执行回转'
                if re.match(u'.*结案.{0,2}通知.{0,2}书', txt):
                    return '结案通知书'
                if re.match(u'.*诉.*.*权.*利.*义.*.*告.*知.*书.*', txt):
                    return '诉讼权利义务告知书'
                if re.match(u'.?核保笔录.?', txt):
                    return '核保笔录'
                if re.match(u'.*诉讼保全案件移送表.?', txt):
                    return '—诉讼保全案件移送表'
                if re.match(u'.?协助[执扰]行通知书.?', txt):
                    return '协助执行通知书'
        if lineNum > 3:
            break
        lineNum = 0
        for y in range(height - 1)[::-1]:
            up = 0
            down = 0
            for i in range(y)[::-1]:
                if int(row[i]) > 1:
                    y = i - 1
                    down = i + 1 if i + 1 < height - 1 else height - 1
                    break
                if i == 0:
                    y = 0
            for i in range(y - 1)[::-1]:
                i = i + 1
                if int(row[i]) <= 1 & int(row[i - 1]) <= 1:
                    y = i
                    up = i - 1 if i - 1 > 0 else 0
                    break
                if i == 0:
                    y = 0
            if float(height * 0.35) > float(down - up) > float(lineHeight):
                lineImage = orignImageFile.crop((0, int(up * 10), int(orignWidth), int(down * 10)))
                # lineImage = lineImage.copy()
                # lineImage.show()
                lineNum = lineNum + 1
                # lineImage.show()
                txt = Ocr(lineImage, type)
                txt = txt.decode('utf-8')
                if re.match(u'账号.{0,2}[\\d]{5,16}|开户行.*|.{1,5}省.{0,3}收[入人].{2,6}', txt):
                    return '缴纳诉讼费'
                if re.match(u'.{0,2}[此北]致.{0,5}|具状.{2,6}|答[辨辩].*|谢谢法庭.*|.{1,9}[耳年].{1,3}[月目用门].{1,4}[口日曰白门]'
                            u'.{0,4}|.{3,10}法[阮院脘][^起诉]{0,4}|.{2,6}[级区]人民法.{1,2}|.{0,1}附.{0,1}|.*光盘.张.{0,2}|[\d]'
                            u'.{0,4}卷宗.{2,4}|.*起诉人:.*|[此北].{1,3}|.{0,2}[上公]诉[人八]:.{1,4}|[申巾]请[人八]:.{0,3}|附:.*'
                            u'|.*法律服务所|.*律[师帅]事务所|.{1,10}律师|.?[窜审]判[长员].{1,5}|被代:.*|负责人：.*|.?社区矫正对.{2,6}'
                            u'|[辨辩]护[人儿].{2,4}|年月[日曰门]|谢谢|检察员:.|.{3,10}人[民尺].?[院浣脘][^起诉]{0,7}|.{2,5}司.局'
                            u'|.{3,9}挥部|.{2,8}办公室.{1,6}[耳年].{0,3}[月目用门].{0,4}[口日曰白门].{0,4}|.{0,4}市.{2,7}民法.?'
                            u'|.{1,6}[耳年].{0,3}[月目用门].?[\d].{0,2}|[\d]{3,5}年.{2,7}|.{1,3}[市币].{1,3}区人民.{1,5}'
                            u'|当事人核对笔录无误.{1,5}', txt):
                    return '文件尾页'
                if re.match(u'委托人.{0,7}|.{0,5}[人居]民.{2,8}证|.*中华.*公安部.*|律师年.{0,2}度.*案.{0,2}|.?执业证.*'
                            u'|.{0,3}[常住人口登记卡]{4,}.{0,4}|[中华人民共和国]{5,}|成立日期.{1,5}[耳年].{0,3}[月目用门].{0,4}[日曰白].{0,3}'
                            u'|.*律师.度.核备案.*|发证[曰日]期.*|.[效姣].限.[\d\w].{0,4}.*|.*度.{0,3}核备.*|中.{0,4}民共和国'
                            u'|签发机关.{0,4}公安局|.{0,2}公民.?份号码[\d]{7,}|.*一[社祉]会信用代.*|登记机关.{0,3}', txt):
                    return '授权委托书、身份证明'
                if re.match(u'.*投递员签.{0,3}|.*代收人签名.*|.*收寄[邮邯]件.*|.*邮件运.*|.*投递并签.*', txt):
                    return '送达回证'
                if re.match(u'.{0,5}收.?条', txt):
                    return '执行通知书存根和回执（释放证回执）'
            if lineNum > 7:
                break
        return ''
        # deepClassifiedInformation = 1
        # fineDocumentNum = fineDocumentNum + 1
        # return deepClassifiedInformation, fineDocumentNum


def contentEndCheck(image, row, imageFile):  # 特殊文件的尾部识别
    lineNum = 0
    height = len(image)
    width = len(image[0])
    lineHeight = int(height / 70)
    for y in range(height - 1)[::-1]:
        up = 0
        down = 0
        for i in range(y)[::-1]:
            if row[i] > 10:
                y = i - 1
                down = i + 5 if i + 5 < height - 1 else height - 1
                break
            if i == 0:
                y = 0
        for i in range(y)[::-1]:
            if row[i] < 13:
                y = i
                up = i - 5 if i - 5 > 0 else 0
                break
            if i == 0:
                y = 0
        if height * 0.5 > down - up > lineHeight:
            lineNum = lineNum + 1
            lineImage = imageFile.crop(0, up, width, down - up)
            txt = Ocr(lineImage, type)
            txt = txt.decode('utf-8')
            if re.match(u'.*为其诉讼代理.{1,3}|.*代理诉讼.{0,3}|.{0,4}授权委[托抚拄]书.{0,5}|.*委托.{0,4}|.{0,5}法律服务.{0,5}',txt):
                return '特定类型的文件尾 - 身份证,委托书'
            if re.match(u'.*撤回.{0,3}执行.{0,4}', txt):
                return '特定类型的文件尾 - 执行撤回'
        if lineNum > 5:
            return '其它'
    return '其它'




def fileEndCheck(image, row, threshlod):
    (width, height) = image.size
    blankLen = 0
    for y in range(height - 1)[::-1]:
        if int(row[y]) > 1 & int(row[y - 1]) > 1:
            break
        blankLen = blankLen + 1
    if blankLen > height * threshlod:
        for y in xrange(height):
            up = 0
            down = 0
            for i in xrange(y, height):
                if int(row[i]) > 1:
                    up = i
                    down = i
                    break
                if i == height - 1:
                    y = height
            for i in xrange(y, height):
                if int(row[i] <= 1):
                    down = i
                    if float(down - up) > float(height * 0.1):
                        return False
                    y = i
                    break
        return True
    return False


def endCheck(image, row, imageFile):  # 文件尾部识别
    lineNum = 0
    (width, height) = image.size
    lineH = int(height / 100)
    for y in range(height)[::-1]:
        up = 0
        down = 0
        for i in range(y)[::-1]:
            if int(row[i]) > 10:
                y = i - 1
                down = i + 1 if i + 1 < height - 1 else height - 1
                break
            if i == 0:
                y = 0
        for i in range(y)[::-1]:
            if int(row[i]) < 13:
                y = i
                up = i - 1 if i - 1 > 0 else 0
                break
            if i == 0:
                y = 0
        if float(lineH) < float(down - up) < float(height * 0.5):
            lineH = lineH + 1
            lineImage = imageFile.crop((0, up, width, down))
            txt = Ocr(lineImage, type)
            if txt:
                txt = txt.decode('utf-8')
            # 此处匹配的文章不太清楚为什么先写框架，后进行修正
                if re.match(u'.{0,2}[此北]致.{0,5}|.{0,2}具状.*|.{0,2}原告人.*|.{0,2}申请.{2,6}|.{0,2}答[辨辩].{2,6}|.{1,8}[耳年].*[月目用门].*[口日曰白门].{0,3}'
                        u'|.{3,10}[人八]民法[阮院].{0,2}|.{0,1}附.{0,1}|.*起诉人:.*|.{1,6}人:.{2,4}|[此北].|.{0,2}[上公]诉[人八]:.{1,4}|[申巾]请[人八]：.{0,3}'
                        u'|.?法定代表.{0,3}[(]印[章童][)]|.*法律服务所|.*律[师帅]事务所|.{1,10}律师|.?[窜审]判[长员].{1,5}|.{2,8}局|负责人:.*|[辨辩]护[人儿].{2,4}'
                        u'|年月[日曰门]|谢谢|检察员:.*|.{2,6}[市巾]级.{0,3}法院.{0,4}', txt):
                    return True
        if lineNum > 4:
            return False
    return False




def wordsFilter(txt):
    pass


if __name__ == '__main__':
    # filePath = r'C:\Users\Administrator\Desktop\no-down'
    # file = os.listdir(filePath)[1:]
    # imageName = os.listdir(filePath + os.path.sep + file[0])
    # imagePath = filePath + os.path.sep + file[0] + os.path.sep + imageName[0]

    imagePath = r'D:\down\2.jpg'
    imageFile = Image.open(imagePath)
    type = u'Abbyy'
    deepClassifiedInformation = fineClassifyDocument(imageFile, type)
    print(deepClassifiedInformation)
