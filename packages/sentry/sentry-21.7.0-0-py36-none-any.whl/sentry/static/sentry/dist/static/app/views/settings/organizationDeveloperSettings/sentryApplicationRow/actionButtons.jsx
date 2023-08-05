Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirmDelete_1 = tslib_1.__importDefault(require("app/components/confirmDelete"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ActionButtons = function (_a) {
    var org = _a.org, app = _a.app, showPublish = _a.showPublish, showDelete = _a.showDelete, onPublish = _a.onPublish, onDelete = _a.onDelete, disablePublishReason = _a.disablePublishReason, disableDeleteReason = _a.disableDeleteReason;
    var appDashboardButton = (<StyledButton size="small" icon={<icons_1.IconStats />} to={"/settings/" + org.slug + "/developer-settings/" + app.slug + "/dashboard/"}>
      {locale_1.t('Dashboard')}
    </StyledButton>);
    var publishRequestButton = showPublish ? (<StyledButton disabled={!!disablePublishReason} title={disablePublishReason} icon={<icons_1.IconUpgrade />} size="small" onClick={onPublish}>
      {locale_1.t('Publish')}
    </StyledButton>) : null;
    var deleteConfirmMessage = locale_1.t("Deleting " + app.slug + " will also delete any and all of its installations.          This is a permanent action. Do you wish to continue?");
    var deleteButton = showDelete ? (disableDeleteReason ? (<StyledButton disabled title={disableDeleteReason} size="small" icon={<icons_1.IconDelete />} label="Delete"/>) : (onDelete && (<confirmDelete_1.default message={deleteConfirmMessage} confirmInput={app.slug} priority="danger" onConfirm={function () { return onDelete(app); }}>
          <StyledButton size="small" icon={<icons_1.IconDelete />} label="Delete"/>
        </confirmDelete_1.default>))) : null;
    return (<ButtonHolder>
      {appDashboardButton}
      {publishRequestButton}
      {deleteButton}
    </ButtonHolder>);
};
var ButtonHolder = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex-direction: row;\n  display: flex;\n  & > * {\n    margin-left: ", ";\n  }\n"], ["\n  flex-direction: row;\n  display: flex;\n  & > * {\n    margin-left: ", ";\n  }\n"])), space_1.default(0.5));
var StyledButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
exports.default = ActionButtons;
var templateObject_1, templateObject_2;
//# sourceMappingURL=actionButtons.jsx.map