Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
function ProjectSourceMapsContainer(props) {
    var children = props.children, organization = props.organization, project = props.project;
    return React.isValidElement(children)
        ? React.cloneElement(children, { organization: organization, project: project })
        : null;
}
exports.default = withOrganization_1.default(ProjectSourceMapsContainer);
//# sourceMappingURL=index.jsx.map