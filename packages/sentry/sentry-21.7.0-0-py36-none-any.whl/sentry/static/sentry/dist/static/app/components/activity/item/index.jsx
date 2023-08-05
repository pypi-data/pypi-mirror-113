Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_timezone_1 = tslib_1.__importDefault(require("moment-timezone"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var text_1 = tslib_1.__importDefault(require("app/styles/text"));
var isRenderFunc_1 = require("app/utils/isRenderFunc");
var avatar_1 = tslib_1.__importDefault(require("./avatar"));
var bubble_1 = tslib_1.__importDefault(require("./bubble"));
function ActivityItem(_a) {
    var author = _a.author, avatarSize = _a.avatarSize, bubbleProps = _a.bubbleProps, className = _a.className, children = _a.children, date = _a.date, interval = _a.interval, footer = _a.footer, id = _a.id, header = _a.header, _b = _a.hideDate, hideDate = _b === void 0 ? false : _b, _c = _a.showTime, showTime = _c === void 0 ? false : _c;
    var showDate = !hideDate && date && !interval;
    var showRange = !hideDate && date && interval;
    var dateEnded = showRange
        ? moment_timezone_1.default(date).add(interval, 'minutes').utc().format()
        : undefined;
    var timeOnly = Boolean(date && dateEnded && moment_timezone_1.default(date).date() === moment_timezone_1.default(dateEnded).date());
    return (<ActivityItemWrapper data-test-id="activity-item" className={className}>
      {id && <a id={id}/>}

      {author && (<StyledActivityAvatar type={author.type} user={author.user} size={avatarSize}/>)}

      <StyledActivityBubble {...bubbleProps}>
        {header && isRenderFunc_1.isRenderFunc(header) && header()}
        {header && !isRenderFunc_1.isRenderFunc(header) && (<ActivityHeader>
            <ActivityHeaderContent>{header}</ActivityHeaderContent>
            {date && showDate && !showTime && <StyledTimeSince date={date}/>}
            {date && showDate && showTime && <StyledDateTime timeOnly date={date}/>}

            {showRange && (<StyledDateTimeWindow>
                <StyledDateTime timeOnly={timeOnly} timeAndDate={!timeOnly} date={date}/>
                {' — '}
                <StyledDateTime timeOnly={timeOnly} timeAndDate={!timeOnly} date={dateEnded}/>
              </StyledDateTimeWindow>)}
          </ActivityHeader>)}

        {children && isRenderFunc_1.isRenderFunc(children) && children()}
        {children && !isRenderFunc_1.isRenderFunc(children) && (<ActivityBody>{children}</ActivityBody>)}

        {footer && isRenderFunc_1.isRenderFunc(footer) && footer()}
        {footer && !isRenderFunc_1.isRenderFunc(footer) && (<ActivityFooter>{footer}</ActivityFooter>)}
      </StyledActivityBubble>
    </ActivityItemWrapper>);
}
var ActivityItemWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  margin-bottom: ", ";\n"])), space_1.default(2));
var HeaderAndFooter = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: 6px ", ";\n"], ["\n  padding: 6px ", ";\n"])), space_1.default(2));
var ActivityHeader = styled_1.default(HeaderAndFooter)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  border-bottom: 1px solid ", ";\n  font-size: ", ";\n\n  &:last-child {\n    border-bottom: none;\n  }\n"], ["\n  display: flex;\n  border-bottom: 1px solid ", ";\n  font-size: ", ";\n\n  &:last-child {\n    border-bottom: none;\n  }\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.fontSizeMedium; });
var ActivityHeaderContent = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var ActivityFooter = styled_1.default(HeaderAndFooter)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  border-top: 1px solid ", ";\n  font-size: ", ";\n"], ["\n  display: flex;\n  border-top: 1px solid ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.fontSizeMedium; });
var ActivityBody = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  ", "\n"], ["\n  padding: ", " ", ";\n  ", "\n"])), space_1.default(2), space_1.default(2), text_1.default);
var StyledActivityAvatar = styled_1.default(avatar_1.default)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var StyledTimeSince = styled_1.default(timeSince_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var StyledDateTime = styled_1.default(dateTime_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var StyledDateTimeWindow = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var StyledActivityBubble = styled_1.default(bubble_1.default)(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  width: 75%;\n  overflow-wrap: break-word;\n"], ["\n  width: 75%;\n  overflow-wrap: break-word;\n"])));
exports.default = ActivityItem;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=index.jsx.map