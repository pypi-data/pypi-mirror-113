Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var locale_1 = require("app/locale");
var actionButtons_1 = tslib_1.__importDefault(require("./actionButtons"));
var SentryApplicationRowButtons = function (_a) {
    var organization = _a.organization, app = _a.app, onClickRemove = _a.onClickRemove, onClickPublish = _a.onClickPublish;
    var isInternal = app.status === 'internal';
    return (<access_1.default access={['org:admin']}>
      {function (_a) {
            var hasAccess = _a.hasAccess;
            var disablePublishReason = '';
            var disableDeleteReason = '';
            // Publish & Delete buttons will always be disabled if the app is published
            if (app.status === 'published') {
                disablePublishReason = locale_1.t('Published integrations cannot be re-published.');
                disableDeleteReason = locale_1.t('Published integrations cannot be removed.');
            }
            else if (!hasAccess) {
                disablePublishReason = locale_1.t('Organization owner permissions are required for this action.');
                disableDeleteReason = locale_1.t('Organization owner permissions are required for this action.');
            }
            return (<actionButtons_1.default org={organization} app={app} showPublish={!isInternal} showDelete onPublish={onClickPublish} onDelete={onClickRemove} disablePublishReason={disablePublishReason} disableDeleteReason={disableDeleteReason}/>);
        }}
    </access_1.default>);
};
exports.default = SentryApplicationRowButtons;
//# sourceMappingURL=sentryApplicationRowButtons.jsx.map