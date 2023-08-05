Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var groupEventAttachments_1 = tslib_1.__importDefault(require("./groupEventAttachments"));
var GroupEventAttachmentsContainer = function (_a) {
    var organization = _a.organization, group = _a.group;
    return (<feature_1.default features={['event-attachments']} organization={organization} renderDisabled={function (props) { return <featureDisabled_1.default {...props}/>; }}>
    <groupEventAttachments_1.default projectSlug={group.project.slug}/>
  </feature_1.default>);
};
exports.default = withOrganization_1.default(GroupEventAttachmentsContainer);
//# sourceMappingURL=index.jsx.map