from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"C:\Users\jiabo\Documents\GitHub\DongSheng-jiabo-11")
OUT = ROOT / "output" / "pdf" / "薄肌健身计划_课程表定制版.pdf"
FONT = r"C:\Windows\Fonts\simhei.ttf"
FONT_BOLD = r"C:\Windows\Fonts\simhei.ttf"
pdfmetrics.registerFont(TTFont("CN", FONT))
pdfmetrics.registerFont(TTFont("CN-Bold", FONT_BOLD))


PAGE_W, PAGE_H = A4
INK = colors.HexColor("#1F2933")
MUTED = colors.HexColor("#52606D")
BLUE = colors.HexColor("#1769AA")
PALE_BLUE = colors.HexColor("#EAF3FB")
PALE_GREEN = colors.HexColor("#EAF7F0")
PALE_YELLOW = colors.HexColor("#FFF7E6")
GRID = colors.HexColor("#D9E2EC")


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="TitleCN", fontName="CN-Bold", fontSize=20, leading=27,
    alignment=TA_CENTER, textColor=INK, spaceAfter=5 * mm,
))
styles.add(ParagraphStyle(
    name="SubCN", fontName="CN", fontSize=9.5, leading=15,
    alignment=TA_CENTER, textColor=MUTED, spaceAfter=4 * mm,
))
styles.add(ParagraphStyle(
    name="H1CN", fontName="CN-Bold", fontSize=14, leading=20,
    textColor=BLUE, spaceBefore=2 * mm, spaceAfter=2 * mm,
))
styles.add(ParagraphStyle(
    name="H2CN", fontName="CN-Bold", fontSize=10.5, leading=15,
    textColor=INK, spaceBefore=1.5 * mm, spaceAfter=1 * mm,
))
styles.add(ParagraphStyle(
    name="BodyCN", fontName="CN", fontSize=9.2, leading=14,
    textColor=INK, spaceAfter=1.6 * mm,
))
styles.add(ParagraphStyle(
    name="SmallCN", fontName="CN", fontSize=8, leading=11,
    textColor=MUTED, spaceAfter=1 * mm,
))
styles.add(ParagraphStyle(
    name="TableCN", fontName="CN", fontSize=8.1, leading=11,
    textColor=INK,
))
styles.add(ParagraphStyle(
    name="TableBoldCN", fontName="CN-Bold", fontSize=8.1, leading=11,
    textColor=INK,
))
styles.add(ParagraphStyle(
    name="BoxCN", fontName="CN", fontSize=8.7, leading=13,
    textColor=INK,
))


def P(text, style="BodyCN"):
    return Paragraph(text, styles[style])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.4)
    canvas.line(16 * mm, 12 * mm, PAGE_W - 16 * mm, 12 * mm)
    canvas.setFont("CN", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(16 * mm, 7 * mm, "课程表定制版 | 目标：线条清晰、力量上升、体重稳定增加")
    canvas.drawRightString(PAGE_W - 16 * mm, 7 * mm, f"第 {doc.page} 页")
    canvas.restoreState()


def make_table(data, widths, header=True, row_bgs=None, font_size=8.1):
    converted = []
    for r, row in enumerate(data):
        converted.append([
            Paragraph(str(cell), styles["TableBoldCN" if header and r == 0 else "TableCN"])
            for cell in row
        ])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        commands += [("BACKGROUND", (0, 0), (-1, 0), PALE_BLUE)]
    if row_bgs:
        for idx, color in row_bgs.items():
            commands.append(("BACKGROUND", (0, idx), (-1, idx), color))
    table.setStyle(TableStyle(commands))
    return table


def section_title(text):
    return [Spacer(1, 2 * mm), P(text, "H1CN")]


story = []
story.append(P("180 cm / 75 kg 新手薄肌训练计划", "TitleCN"))
story.append(P("根据 2026-2027 秋季学期课程表定制 | 健身房营业 08:00-22:00", "SubCN"))

profile = [
    ["你的条件", "本计划的执行口径"],
    ["20 岁，180 cm，75 kg", "按“精瘦、线条清晰、力量稳步上升”设计，不追求快速增重"],
    ["有健身房，已有蛋白粉", "优先使用固定器械和哑铃，动作更容易控制；蛋白粉只是补充，不是主食"],
    ["新手", "前两周每周 3 次；第 3 周起恢复良好再增加到 4 次"],
]
story.append(make_table(profile, [38 * mm, 132 * mm], row_bgs={1: PALE_GREEN, 3: PALE_YELLOW}))
story.append(Spacer(1, 3 * mm))
story.append(P("先记住一句话：薄肌不是“少吃少练”，而是用可控热量、足够蛋白和渐进负重，把肌肉长在不明显增脂的速度上。", "BoxCN"))

story += section_title("一、每周安排：直接照着课表走")
weekly = [
    ["星期", "课程表中的关键空档", "训练安排", "建议时间"],
    ["周一", "12:00 后至晚课前较空", "上肢 A", "16:40-17:50"],
    ["周二", "10:20-20:10 多段课程", "休息 + 10 分钟拉伸", "晚课后不硬练"],
    ["周三", "17:05 后空", "下肢 A", "17:30-18:40"],
    ["周四", "10:20-20:10 多段课程", "休息 + 散步 20-30 分钟", "不安排力量训练"],
    ["周五", "15:25-17:05 后，20:25 前", "上肢 B", "17:30-18:35"],
    ["周六", "白天空，20:25 有线上课", "休息；可散步", "白天不补课式训练"],
    ["周日", "基本空闲", "下肢 B", "10:00-11:10"],
]
story.append(make_table(weekly, [18 * mm, 62 * mm, 42 * mm, 48 * mm], row_bgs={1: PALE_GREEN, 3: PALE_GREEN, 5: PALE_GREEN, 7: PALE_GREEN}))
story.append(Spacer(1, 2 * mm))
story.append(P("前两周只做周一、周三、周五三次训练。第三周开始，如果睡眠正常、酸痛不影响上课、训练重量能稳定完成，再加入周日下肢 B。", "SmallCN"))

story += section_title("二、每次训练怎么做")
story.append(P("热身：跑步机快走或单车 5-8 分钟，再用第一个动作做 2 组很轻的热身。正式组保留 2-3 次余力（RIR 2-3），不要一上来练到力竭。大动作组间休息 90-120 秒，小动作休息 60-90 秒。", "BodyCN"))

upper_a = [
    ["动作", "组数 x 次数", "执行要点"],
    ["坐姿胸推", "3 x 8-12", "肩胛骨收紧，胸口发力，不耸肩"],
    ["高位下拉", "3 x 8-12", "拉到上胸，身体不要大幅后仰"],
    ["坐姿划船", "3 x 8-12", "先收肩胛，再拉肘，不用腰甩"],
    ["哑铃肩推", "2 x 8-12", "腰背贴稳，动作全程可控"],
    ["绳索侧平举", "2 x 12-15", "轻重量，手肘带动，避免耸肩"],
    ["绳索下压 + 哑铃弯举", "各 2 x 10-15", "二头和三头各做一项，干净完成"],
]
lower_a = [
    ["动作", "组数 x 次数", "执行要点"],
    ["腿举", "3 x 8-12", "膝盖方向跟脚尖一致，不要塌腰"],
    ["哑铃罗马尼亚硬拉", "3 x 8-10", "髋部向后，感受大腿后侧拉伸"],
    ["坐姿腿弯举", "2 x 10-15", "顶峰收缩 1 秒，不要弹起"],
    ["保加利亚分腿蹲", "2 x 8-12/侧", "先徒手练稳，再逐步加哑铃"],
    ["站姿提踵", "3 x 12-15", "底部拉伸，顶部停 1 秒"],
    ["平板支撑", "3 x 30-45 秒", "肋骨收紧，腰不要塌"],
]
upper_b = [
    ["动作", "组数 x 次数", "执行要点"],
    ["上斜胸推器械", "3 x 8-12", "椅背略上斜，胸部主导"],
    ["辅助引体或高位下拉", "3 x 8-12", "先下压肩胛，再拉肘"],
    ["胸托划船", "3 x 8-12", "胸口贴稳，避免身体借力"],
    ["器械肩推", "2 x 8-12", "不追求大重量，保持肩关节舒服"],
    ["反向飞鸟", "2 x 12-15", "后束发力，手臂只是传力"],
    ["EZ 杠弯举 + 头顶臂屈伸", "各 2 x 10-15", "肘部尽量固定"],
]
lower_b = [
    ["动作", "组数 x 次数", "执行要点"],
    ["高脚杯深蹲或哈克深蹲", "3 x 8-12", "先练深度和稳定，再加重量"],
    ["臀推", "3 x 8-12", "顶部收紧臀部，不要过度挺腰"],
    ["腿屈伸", "2 x 12-15", "轻重量控制离心"],
    ["坐姿腿弯举", "2 x 10-15", "完整活动范围"],
    ["坐姿提踵", "3 x 12-15", "脚踝充分活动"],
    ["死虫", "3 x 10/侧", "腰背贴地，慢速完成"],
]

for title, table in [("上肢 A：周一", upper_a), ("下肢 A：周三", lower_a), ("上肢 B：周五", upper_b), ("下肢 B：周日", lower_b)]:
    story.append(KeepTogether([
        P(title, "H2CN"),
        make_table(table, [57 * mm, 32 * mm, 81 * mm], row_bgs={1: PALE_GREEN}),
        Spacer(1, 1.5 * mm),
    ]))

story.append(PageBreak())
story += section_title("三、进阶规则：不靠感觉乱加重量")
progress = [
    ["什么时候加重量", "怎么加", "不满足时怎么办"],
    ["某动作所有正式组都达到次数上限，且动作稳定", "上肢加 2.5%-5%；下肢加 5%-10%", "保持原重量，争取下次多完成 1 次"],
    ["连续两次训练动作变形或关节不舒服", "降低 10%-15% 重量，重新练动作", "疼痛持续或加重时停止该动作并就医"],
    ["一周睡眠差、课程压力大、酸痛明显", "当周每个动作少做 1 组", "保留训练习惯，不追求硬撑"],
]
story.append(make_table(progress, [62 * mm, 55 * mm, 53 * mm], row_bgs={1: PALE_GREEN, 2: PALE_YELLOW}))
story.append(P("记录方法：每次记下动作、重量、次数和主观难度。目标不是每次都刷新重量，而是 8-12 周后大多数动作都比第一周更稳定。", "BodyCN"))

story += section_title("四、吃什么：先从小幅盈余开始")
nutrition = [
    ["项目", "你的起始目标", "简单执行"],
    ["蛋白质", "每天约 120-150 g", "三餐各放一掌心肉蛋奶豆；蛋白粉补足缺口"],
    ["热量", "先在当前饮食上增加约 150-250 kcal/天", "连续 2 周记录体重和腰围，再决定是否调整"],
    ["体重速度", "每周增加约 0-0.2 kg", "超过这个速度且腰围涨快，就减少一点热量"],
    ["训练前", "训练前 1-2 小时吃碳水 + 蛋白", "香蕉/面包 + 牛奶/酸奶；不要空腹硬练"],
    ["训练后", "优先吃正常一餐", "若 1-2 小时内吃不了饭，可喝一份蛋白粉"],
]
story.append(make_table(nutrition, [34 * mm, 60 * mm, 76 * mm], row_bgs={1: PALE_GREEN, 3: PALE_YELLOW}))
story.append(Spacer(1, 2 * mm))
story.append(P("一日示例：早餐燕麦 + 鸡蛋 + 牛奶；午餐米饭 + 鸡腿/牛肉 + 蔬菜；训练前香蕉 + 酸奶；训练后正常晚餐，必要时补蛋白粉；睡前可用牛奶或无糖酸奶补充。蛋白粉不是药，喝了也不会自动长肌肉，训练和总饮食才是主角。", "BodyCN"))

story += section_title("五、恢复与安全")
recovery = [
    ["睡眠", "尽量保证每晚 7.5-9 小时。周二、周四课程较满，训练量已经由课程表限制，不要为了凑次数熬夜。"],
    ["有氧", "每周 2-3 次轻松快走 20-30 分钟即可，放在休息日或训练后；目标是心肺和恢复，不是把自己跑空。"],
    ["疼痛", "肌肉酸胀可以观察；关节刺痛、胸痛、头晕、异常呼吸困难应立即停止训练并寻求专业医疗帮助。"],
    ["器械学习", "第一次使用不熟悉器械时，先让教练或工作人员确认座椅高度、活动范围和安全销位置。"],
]
story.append(make_table([["事项", "执行要求"]] + recovery, [25 * mm, 145 * mm], row_bgs={1: PALE_GREEN, 3: PALE_YELLOW}))

story += section_title("六、两周检查点")
story.append(P("第 14 天只检查三件事：是否完成至少 5 次训练；主要动作是否比第一周更稳；体重和腰围是否快速上升。如果训练完成率低于 70%，先缩短训练到 45-60 分钟，不要继续加动作。", "BodyCN"))

story += section_title("资料依据")
story.append(P("训练频率、渐进负重和动作安排参考：American College of Sports Medicine, Progression Models in Resistance Training for Healthy Adults, Medicine & Science in Sports & Exercise, 2009, 41(3): 687-708, DOI: 10.1249/MSS.0b013e3181915670。蛋白质范围参考：Jäger et al., International Society of Sports Nutrition Position Stand: Protein and Exercise, Journal of the International Society of Sports Nutrition, 2017, 14:20, DOI: 10.1186/s12970-017-0177-8。", "SmallCN"))
story.append(P("课程表事实来源：用户提供的《课程表.pdf》，显示为 2026-2027 学年秋季学期课程表，打印日期 2026-09-26。本文件把课程表当作时间安排数据，不把其中内容当作训练指令。", "SmallCN"))

OUT.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, rightMargin=16 * mm, leftMargin=16 * mm,
    topMargin=14 * mm, bottomMargin=16 * mm,
    title="180 cm / 75 kg 新手薄肌训练计划",
    author="Codex",
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
