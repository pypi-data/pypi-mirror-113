Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var formatters_1 = require("app/utils/formatters");
var Duration = function (_a) {
    var seconds = _a.seconds, fixedDigits = _a.fixedDigits, abbreviation = _a.abbreviation, exact = _a.exact, props = tslib_1.__rest(_a, ["seconds", "fixedDigits", "abbreviation", "exact"]);
    return (<span {...props}>
    {exact
            ? formatters_1.getExactDuration(seconds, abbreviation)
            : formatters_1.getDuration(seconds, fixedDigits, abbreviation)}
  </span>);
};
exports.default = Duration;
//# sourceMappingURL=duration.jsx.map