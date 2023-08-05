Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var highlight_1 = tslib_1.__importDefault(require("app/components/highlight"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var utils_1 = require("app/utils");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var utils_2 = require("./utils");
var Time = react_1.memo(function (_a) {
    var timestamp = _a.timestamp, relativeTime = _a.relativeTime, displayRelativeTime = _a.displayRelativeTime, searchTerm = _a.searchTerm;
    if (!(utils_1.defined(timestamp) && utils_1.defined(relativeTime))) {
        return null;
    }
    var _b = utils_2.getFormattedTimestamp(timestamp, relativeTime, displayRelativeTime), date = _b.date, time = _b.time, displayTime = _b.displayTime;
    return (<Wrapper>
      <tooltip_1.default title={<div>
            <div>{date}</div>
            {time !== '\u2014' && <div>{time}</div>}
          </div>} containerDisplayMode="inline-flex" disableForVisualTest>
        <textOverflow_1.default>
          {getDynamicText_1.default({
            value: <highlight_1.default text={searchTerm}>{displayTime}</highlight_1.default>,
            fixed: '00:00:00',
        })}
        </textOverflow_1.default>
      </tooltip_1.default>
    </Wrapper>);
});
exports.default = Time;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.textColor; });
var templateObject_1;
//# sourceMappingURL=index.jsx.map