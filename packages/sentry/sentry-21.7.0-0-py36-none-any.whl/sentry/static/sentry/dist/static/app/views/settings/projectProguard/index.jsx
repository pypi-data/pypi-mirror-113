Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var projectProguard_1 = tslib_1.__importDefault(require("./projectProguard"));
var ProjectProguardContainer = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectProguardContainer, _super);
    function ProjectProguardContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectProguardContainer.prototype.render = function () {
        return <projectProguard_1.default {...this.props}/>;
    };
    return ProjectProguardContainer;
}(react_1.Component));
exports.default = withOrganization_1.default(ProjectProguardContainer);
//# sourceMappingURL=index.jsx.map