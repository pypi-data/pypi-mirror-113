Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var constants_1 = require("app/constants");
var selectorItem_1 = tslib_1.__importDefault(require("./selectorItem"));
var RelativeSelector = function (_a) {
    var onClick = _a.onClick, selected = _a.selected, relativePeriods = _a.relativePeriods;
    return (<React.Fragment>
    {Object.entries(relativePeriods || constants_1.DEFAULT_RELATIVE_PERIODS).map(function (_a) {
            var _b = tslib_1.__read(_a, 2), value = _b[0], label = _b[1];
            return (<selectorItem_1.default key={value} onClick={onClick} value={value} label={label} selected={selected === value}/>);
        })}
  </React.Fragment>);
};
exports.default = RelativeSelector;
//# sourceMappingURL=relativeSelector.jsx.map