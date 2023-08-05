Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var projectPerformance_1 = tslib_1.__importDefault(require("./projectPerformance"));
var ProjectPerformanceContainer = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectPerformanceContainer, _super);
    function ProjectPerformanceContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectPerformanceContainer.prototype.render = function () {
        return (<feature_1.default features={['project-transaction-threshold']}>
        <projectPerformance_1.default {...this.props}/>
      </feature_1.default>);
    };
    return ProjectPerformanceContainer;
}(react_1.default.Component));
exports.default = withOrganization_1.default(ProjectPerformanceContainer);
//# sourceMappingURL=index.jsx.map