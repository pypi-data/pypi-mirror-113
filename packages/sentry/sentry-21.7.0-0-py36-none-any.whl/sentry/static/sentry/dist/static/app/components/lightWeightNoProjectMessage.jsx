Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var noProjectMessage_1 = tslib_1.__importDefault(require("app/components/noProjectMessage"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var LightWeightNoProjectMessage = /** @class */ (function (_super) {
    tslib_1.__extends(LightWeightNoProjectMessage, _super);
    function LightWeightNoProjectMessage() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LightWeightNoProjectMessage.prototype.render = function () {
        var _a = this.props, organization = _a.organization, projects = _a.projects, loadingProjects = _a.loadingProjects;
        return (<noProjectMessage_1.default {...this.props} projects={projects} loadingProjects={!('projects' in organization) && loadingProjects}/>);
    };
    return LightWeightNoProjectMessage;
}(react_1.Component));
exports.default = withProjects_1.default(LightWeightNoProjectMessage);
//# sourceMappingURL=lightWeightNoProjectMessage.jsx.map