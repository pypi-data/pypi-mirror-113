Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var projectDetail_1 = tslib_1.__importDefault(require("./projectDetail"));
function ProjectDetailContainer(props) {
    return <projectDetail_1.default {...props}/>;
}
exports.default = withOrganization_1.default(ProjectDetailContainer);
//# sourceMappingURL=index.jsx.map