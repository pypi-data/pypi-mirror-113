Object.defineProperty(exports, "__esModule", { value: true });
exports.RingText = exports.RingBar = exports.RingBackground = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var testableTransition_1 = tslib_1.__importDefault(require("app/utils/testableTransition"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var Text = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 100%;\n  width: 100%;\n  color: ", ";\n  font-size: ", ";\n  padding-top: 1px;\n  transition: color 100ms;\n  ", "\n"], ["\n  position: absolute;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 100%;\n  width: 100%;\n  color: ", ";\n  font-size: ", ";\n  padding-top: 1px;\n  transition: color 100ms;\n  ", "\n"])), function (p) { return p.theme.chartLabel; }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.textCss && p.textCss(p); });
exports.RingText = Text;
var AnimatedText = framer_motion_1.motion(Text);
AnimatedText.defaultProps = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 10 },
    transition: testableTransition_1.default(),
};
var ProgressRing = function (_a) {
    var value = _a.value, _b = _a.minValue, minValue = _b === void 0 ? 0 : _b, _c = _a.maxValue, maxValue = _c === void 0 ? 100 : _c, _d = _a.size, size = _d === void 0 ? 20 : _d, _e = _a.barWidth, barWidth = _e === void 0 ? 3 : _e, text = _a.text, textCss = _a.textCss, _f = _a.animateText, animateText = _f === void 0 ? false : _f, _g = _a.progressColor, progressColor = _g === void 0 ? theme_1.default.green300 : _g, _h = _a.backgroundColor, backgroundColor = _h === void 0 ? theme_1.default.gray200 : _h, progressEndcaps = _a.progressEndcaps, p = tslib_1.__rest(_a, ["value", "minValue", "maxValue", "size", "barWidth", "text", "textCss", "animateText", "progressColor", "backgroundColor", "progressEndcaps"]);
    var radius = size / 2 - barWidth / 2;
    var circumference = 2 * Math.PI * radius;
    var boundedValue = Math.min(Math.max(value, minValue), maxValue);
    var progress = (boundedValue - minValue) / (maxValue - minValue);
    var percent = progress * 100;
    var progressOffset = (1 - progress) * circumference;
    var TextComponent = animateText ? AnimatedText : Text;
    var textNode = (<TextComponent key={text === null || text === void 0 ? void 0 : text.toString()} {...{ textCss: textCss, percent: percent }}>
      {text}
    </TextComponent>);
    textNode = animateText ? (<framer_motion_1.AnimatePresence initial={false}>{textNode}</framer_motion_1.AnimatePresence>) : (textNode);
    return (<RingSvg height={radius * 2 + barWidth} width={radius * 2 + barWidth} {...p}>
      <RingBackground r={radius} barWidth={barWidth} cx={radius + barWidth / 2} cy={radius + barWidth / 2} color={backgroundColor}/>
      <RingBar strokeDashoffset={progressOffset} strokeLinecap={progressEndcaps} circumference={circumference} r={radius} barWidth={barWidth} cx={radius + barWidth / 2} cy={radius + barWidth / 2} color={progressColor}/>
      <foreignObject height="100%" width="100%">
        {text !== undefined && textNode}
      </foreignObject>
    </RingSvg>);
};
var RingSvg = styled_1.default('svg')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var RingBackground = styled_1.default('circle')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  fill: none;\n  stroke: ", ";\n  stroke-width: ", "px;\n  transition: stroke 100ms;\n"], ["\n  fill: none;\n  stroke: ", ";\n  stroke-width: ", "px;\n  transition: stroke 100ms;\n"])), function (p) { return p.color; }, function (p) { return p.barWidth; });
exports.RingBackground = RingBackground;
var RingBar = styled_1.default('circle')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  fill: none;\n  stroke: ", ";\n  stroke-width: ", "px;\n  stroke-dasharray: ", " ", ";\n  transform: rotate(-90deg);\n  transform-origin: 50% 50%;\n  transition: stroke-dashoffset 200ms, stroke 100ms;\n"], ["\n  fill: none;\n  stroke: ", ";\n  stroke-width: ", "px;\n  stroke-dasharray: ", " ", ";\n  transform: rotate(-90deg);\n  transform-origin: 50% 50%;\n  transition: stroke-dashoffset 200ms, stroke 100ms;\n"])), function (p) { return p.color; }, function (p) { return p.barWidth; }, function (p) { return p.circumference; }, function (p) { return p.circumference; });
exports.RingBar = RingBar;
exports.default = ProgressRing;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=progressRing.jsx.map