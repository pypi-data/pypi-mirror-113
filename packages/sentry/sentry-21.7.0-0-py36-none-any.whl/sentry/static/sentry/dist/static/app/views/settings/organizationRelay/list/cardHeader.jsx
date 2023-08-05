Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var clipboard_1 = tslib_1.__importDefault(require("app/components/clipboard"));
var confirmDelete_1 = tslib_1.__importDefault(require("app/components/confirmDelete"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var CardHeader = function (_a) {
    var publicKey = _a.publicKey, name = _a.name, description = _a.description, created = _a.created, disabled = _a.disabled, onEdit = _a.onEdit, onDelete = _a.onDelete;
    var deleteButton = (<button_1.default size="small" icon={<icons_1.IconDelete />} label={locale_1.t('Delete Key')} disabled={disabled} title={disabled ? locale_1.t('You do not have permission to delete keys') : undefined}/>);
    return (<Header>
      <MainInfo>
        <Name>
          <div>{name}</div>
          {description && (<questionTooltip_1.default position="top" size="sm" title={description}/>)}
        </Name>
        <Date>
          {locale_1.tct('Created on [date]', { date: <dateTime_1.default date={created} timeAndDate/> })}
        </Date>
      </MainInfo>
      <buttonBar_1.default gap={1}>
        <clipboard_1.default value={publicKey}>
          <button_1.default size="small" icon={<icons_1.IconCopy />}>
            {locale_1.t('Copy Key')}
          </button_1.default>
        </clipboard_1.default>
        <button_1.default size="small" onClick={onEdit(publicKey)} icon={<icons_1.IconEdit />} label={locale_1.t('Edit Key')} disabled={disabled} title={disabled ? locale_1.t('You do not have permission to edit keys') : undefined}/>
        {disabled ? (deleteButton) : (<confirmDelete_1.default message={locale_1.t('After removing this Public Key, your Relay will no longer be able to communicate with Sentry and events will be dropped.')} onConfirm={onDelete(publicKey)} confirmInput={name}>
            {deleteButton}
          </confirmDelete_1.default>)}
      </buttonBar_1.default>
    </Header>);
};
exports.default = CardHeader;
var Name = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"])), space_1.default(0.5));
var MainInfo = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  color: ", ";\n  display: grid;\n  grid-gap: ", ";\n"])), function (p) { return p.theme.textColor; }, space_1.default(1));
var Date = styled_1.default('small')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; });
var Header = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  align-items: flex-start;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr max-content;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  align-items: flex-start;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr max-content;\n  }\n"])), space_1.default(1), function (p) { return p.theme.breakpoints[0]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=cardHeader.jsx.map