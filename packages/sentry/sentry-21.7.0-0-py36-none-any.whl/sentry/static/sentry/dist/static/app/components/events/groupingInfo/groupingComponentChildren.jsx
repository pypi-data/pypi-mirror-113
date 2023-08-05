Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var isObject_1 = tslib_1.__importDefault(require("lodash/isObject"));
var groupingComponent_1 = tslib_1.__importStar(require("./groupingComponent"));
var utils_1 = require("./utils");
var GroupingComponentChildren = function (_a) {
    var component = _a.component, showNonContributing = _a.showNonContributing;
    return (<react_1.Fragment>
      {component.values
            .filter(function (value) { return utils_1.groupingComponentFilter(value, showNonContributing); })
            .map(function (value, idx) { return (<groupingComponent_1.GroupingComponentListItem key={idx}>
            {isObject_1.default(value) ? (<groupingComponent_1.default component={value} showNonContributing={showNonContributing}/>) : (<groupingComponent_1.GroupingValue valueType={component.name || component.id}>
                {typeof value === 'string' || typeof value === 'number'
                    ? value
                    : JSON.stringify(value, null, 2)}
              </groupingComponent_1.GroupingValue>)}
          </groupingComponent_1.GroupingComponentListItem>); })}
    </react_1.Fragment>);
};
exports.default = GroupingComponentChildren;
//# sourceMappingURL=groupingComponentChildren.jsx.map