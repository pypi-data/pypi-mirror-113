Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var role_1 = tslib_1.__importDefault(require("app/components/acl/role"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var fileSize_1 = tslib_1.__importDefault(require("app/components/fileSize"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ProjectProguardRow = function (_a) {
    var mapping = _a.mapping, onDelete = _a.onDelete, downloadUrl = _a.downloadUrl, downloadRole = _a.downloadRole;
    var id = mapping.id, debugId = mapping.debugId, uuid = mapping.uuid, size = mapping.size, dateCreated = mapping.dateCreated;
    var handleDeleteClick = function () {
        onDelete(id);
    };
    return (<react_1.Fragment>
      <NameColumn>
        <Name>{debugId || uuid || "(" + locale_1.t('empty') + ")"}</Name>
        <TimeWrapper>
          <icons_1.IconClock size="sm"/>
          <timeSince_1.default date={dateCreated}/>
        </TimeWrapper>
      </NameColumn>
      <SizeColumn>
        <fileSize_1.default bytes={size}/>
      </SizeColumn>
      <ActionsColumn>
        <buttonBar_1.default gap={0.5}>
          <role_1.default role={downloadRole}>
            {function (_a) {
            var hasRole = _a.hasRole;
            return (<tooltip_1.default title={locale_1.t('You do not have permission to download mappings.')} disabled={hasRole}>
                <button_1.default size="small" icon={<icons_1.IconDownload size="sm"/>} disabled={!hasRole} href={downloadUrl} title={hasRole ? locale_1.t('Download Mapping') : undefined}/>
              </tooltip_1.default>);
        }}
          </role_1.default>

          <access_1.default access={['project:releases']}>
            {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<tooltip_1.default disabled={hasAccess} title={locale_1.t('You do not have permission to delete mappings.')}>
                <confirm_1.default message={locale_1.t('Are you sure you want to remove this mapping?')} onConfirm={handleDeleteClick} disabled={!hasAccess}>
                  <button_1.default size="small" icon={<icons_1.IconDelete size="sm"/>} title={hasAccess ? locale_1.t('Remove Mapping') : undefined} label={locale_1.t('Remove Mapping')} disabled={!hasAccess}/>
                </confirm_1.default>
              </tooltip_1.default>);
        }}
          </access_1.default>
        </buttonBar_1.default>
      </ActionsColumn>
    </react_1.Fragment>);
};
var NameColumn = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: center;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: center;\n"])));
var SizeColumn = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  text-align: right;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  text-align: right;\n  align-items: center;\n"])));
var ActionsColumn = styled_1.default(SizeColumn)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject([""], [""])));
var Name = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  padding-right: ", ";\n  overflow-wrap: break-word;\n  word-break: break-all;\n"], ["\n  padding-right: ", ";\n  overflow-wrap: break-word;\n  word-break: break-all;\n"])), space_1.default(4));
var TimeWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content 1fr;\n  font-size: ", ";\n  align-items: center;\n  color: ", ";\n  margin-top: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content 1fr;\n  font-size: ", ";\n  align-items: center;\n  color: ", ";\n  margin-top: ", ";\n"])), space_1.default(0.5), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; }, space_1.default(1));
exports.default = ProjectProguardRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=projectProguardRow.jsx.map