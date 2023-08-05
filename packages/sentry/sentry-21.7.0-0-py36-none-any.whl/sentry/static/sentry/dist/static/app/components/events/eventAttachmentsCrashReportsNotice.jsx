Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var groupEventAttachmentsFilter_1 = require("app/views/organizationGroupDetails/groupEventAttachments/groupEventAttachmentsFilter");
var alert_1 = tslib_1.__importDefault(require("../alert"));
var link_1 = tslib_1.__importDefault(require("../links/link"));
var EventAttachmentsCrashReportsNotice = function (_a) {
    var orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, location = _a.location, groupId = _a.groupId;
    var settingsUrl = "/settings/" + orgSlug + "/projects/" + projectSlug + "/security-and-privacy/";
    var attachmentsUrl = {
        pathname: "/organizations/" + orgSlug + "/issues/" + groupId + "/attachments/",
        query: tslib_1.__assign(tslib_1.__assign({}, location.query), { types: groupEventAttachmentsFilter_1.crashReportTypes }),
    };
    return (<alert_1.default type="info" icon={<icons_1.IconInfo size="md"/>}>
      {locale_1.tct('Your limit of stored crash reports has been reached for this issue. [attachmentsLink: View crashes] or [settingsLink: configure limit].', {
            attachmentsLink: <link_1.default to={attachmentsUrl} data-test-id="attachmentsLink"/>,
            settingsLink: <link_1.default to={settingsUrl} data-test-id="settingsLink"/>,
        })}
    </alert_1.default>);
};
exports.default = EventAttachmentsCrashReportsNotice;
//# sourceMappingURL=eventAttachmentsCrashReportsNotice.jsx.map