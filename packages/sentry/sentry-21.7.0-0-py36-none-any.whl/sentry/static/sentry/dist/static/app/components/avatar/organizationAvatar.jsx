Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var baseAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/baseAvatar"));
var utils_1 = require("app/utils");
var OrganizationAvatar = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationAvatar, _super);
    function OrganizationAvatar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationAvatar.prototype.render = function () {
        var _a = this.props, organization = _a.organization, props = tslib_1.__rest(_a, ["organization"]);
        if (!organization) {
            return null;
        }
        var slug = (organization && organization.slug) || '';
        var title = utils_1.explodeSlug(slug);
        return (<baseAvatar_1.default {...props} type={(organization.avatar && organization.avatar.avatarType) || 'letter_avatar'} uploadPath="organization-avatar" uploadId={organization.avatar && organization.avatar.avatarUuid} letterId={slug} tooltip={slug} title={title}/>);
    };
    return OrganizationAvatar;
}(react_1.Component));
exports.default = OrganizationAvatar;
//# sourceMappingURL=organizationAvatar.jsx.map