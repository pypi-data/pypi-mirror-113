Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var ScoreBar = function (_a) {
    var score = _a.score, className = _a.className, vertical = _a.vertical, _b = _a.size, size = _b === void 0 ? 40 : _b, _c = _a.thickness, thickness = _c === void 0 ? 4 : _c, _d = _a.radius, radius = _d === void 0 ? 3 : _d, _e = _a.palette, palette = _e === void 0 ? theme_1.default.similarity.colors : _e;
    var maxScore = palette.length;
    // Make sure score is between 0 and maxScore
    var scoreInBounds = score >= maxScore ? maxScore : score <= 0 ? 0 : score;
    // Make sure paletteIndex is 0 based
    var paletteIndex = scoreInBounds - 1;
    // Size of bar, depends on orientation, although we could just apply a transformation via css
    var barProps = {
        vertical: vertical,
        thickness: thickness,
        size: size,
        radius: radius,
    };
    return (<div className={className}>
      {tslib_1.__spreadArray([], tslib_1.__read(Array(scoreInBounds))).map(function (_j, i) { return (<Bar {...barProps} key={i} color={palette[paletteIndex]}/>); })}
      {tslib_1.__spreadArray([], tslib_1.__read(Array(maxScore - scoreInBounds))).map(function (_j, i) { return (<Bar key={"empty-" + i} {...barProps} empty/>); })}
    </div>);
};
var StyledScoreBar = styled_1.default(ScoreBar)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n\n  ", ";\n"], ["\n  display: flex;\n\n  ", ";\n"])), function (p) {
    return p.vertical
        ? "flex-direction: column-reverse;\n    justify-content: flex-end;"
        : 'min-width: 80px;';
});
var Bar = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-radius: ", "px;\n  margin: 2px;\n  ", ";\n  ", ";\n\n  width: ", "px;\n  height: ", "px;\n"], ["\n  border-radius: ", "px;\n  margin: 2px;\n  ", ";\n  ", ";\n\n  width: ", "px;\n  height: ", "px;\n"])), function (p) { return p.radius; }, function (p) { return p.empty && "background-color: " + p.theme.similarity.empty + ";"; }, function (p) { return p.color && "background-color: " + p.color + ";"; }, function (p) { return (!p.vertical ? p.thickness : p.size); }, function (p) { return (!p.vertical ? p.size : p.thickness); });
exports.default = StyledScoreBar;
var templateObject_1, templateObject_2;
//# sourceMappingURL=scoreBar.jsx.map