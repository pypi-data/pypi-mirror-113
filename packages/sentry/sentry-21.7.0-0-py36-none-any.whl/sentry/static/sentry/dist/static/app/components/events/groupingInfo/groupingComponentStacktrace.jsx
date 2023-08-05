Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var groupingComponent_1 = tslib_1.__importDefault(require("./groupingComponent"));
var groupingComponentFrames_1 = tslib_1.__importDefault(require("./groupingComponentFrames"));
var utils_1 = require("./utils");
var GroupingComponentStacktrace = function (_a) {
    var component = _a.component, showNonContributing = _a.showNonContributing;
    var getFrameGroups = function () {
        var frameGroups = [];
        component.values
            .filter(function (value) { return utils_1.groupingComponentFilter(value, showNonContributing); })
            .forEach(function (value) {
            var key = value.values
                .filter(function (v) { return utils_1.groupingComponentFilter(v, showNonContributing); })
                .map(function (v) { return v.id; })
                .sort(function (a, b) { return a.localeCompare(b); })
                .join('');
            var lastGroup = frameGroups[frameGroups.length - 1];
            if ((lastGroup === null || lastGroup === void 0 ? void 0 : lastGroup.key) === key) {
                lastGroup.data.push(value);
            }
            else {
                frameGroups.push({ key: key, data: [value] });
            }
        });
        return frameGroups;
    };
    return (<react_1.Fragment>
      {getFrameGroups().map(function (group, index) { return (<groupingComponentFrames_1.default key={index} items={group.data.map(function (v, idx) { return (<groupingComponent_1.default key={idx} component={v} showNonContributing={showNonContributing}/>); })}/>); })}
    </react_1.Fragment>);
};
exports.default = GroupingComponentStacktrace;
//# sourceMappingURL=groupingComponentStacktrace.jsx.map