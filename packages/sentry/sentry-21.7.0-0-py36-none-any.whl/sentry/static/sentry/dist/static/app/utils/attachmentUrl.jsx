Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var role_1 = tslib_1.__importDefault(require("app/components/acl/role"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
function AttachmentUrl(_a) {
    var attachment = _a.attachment, organization = _a.organization, eventId = _a.eventId, projectId = _a.projectId, children = _a.children;
    function getDownloadUrl() {
        return "/api/0/projects/" + organization.slug + "/" + projectId + "/events/" + eventId + "/attachments/" + attachment.id + "/";
    }
    return (<role_1.default role={organization.attachmentsRole}>
      {function (_a) {
        var hasRole = _a.hasRole;
        return children(hasRole ? getDownloadUrl() : null);
    }}
    </role_1.default>);
}
exports.default = withOrganization_1.default(react_1.memo(AttachmentUrl));
//# sourceMappingURL=attachmentUrl.jsx.map