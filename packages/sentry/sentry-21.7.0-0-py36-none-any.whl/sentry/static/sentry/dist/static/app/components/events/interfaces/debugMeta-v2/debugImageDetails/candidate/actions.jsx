Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var role_1 = tslib_1.__importDefault(require("app/components/acl/role"));
var button_1 = tslib_1.__importDefault(require("app/components/actions/button"));
var menuItemActionLink_1 = tslib_1.__importDefault(require("app/components/actions/menuItemActionLink"));
var button_2 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var debugImage_1 = require("app/types/debugImage");
var noPermissionToDownloadDebugFilesInfo = locale_1.t('You do not have permission to download debug files');
var noPermissionToDeleteDebugFilesInfo = locale_1.t('You do not have permission to delete debug files');
var debugFileDeleteConfirmationInfo = locale_1.t('Are you sure you wish to delete this file?');
function Actions(_a) {
    var candidate = _a.candidate, organization = _a.organization, isInternalSource = _a.isInternalSource, baseUrl = _a.baseUrl, projectId = _a.projectId, onDelete = _a.onDelete;
    var download = candidate.download, debugFileId = candidate.location;
    var status = download.status;
    if (!debugFileId || !isInternalSource) {
        return null;
    }
    var deleted = status === debugImage_1.CandidateDownloadStatus.DELETED;
    var downloadUrl = baseUrl + "/projects/" + organization.slug + "/" + projectId + "/files/dsyms/?id=" + debugFileId;
    var actions = (<role_1.default role={organization.debugFilesRole} organization={organization}>
      {function (_a) {
            var hasRole = _a.hasRole;
            return (<access_1.default access={['project:write']} organization={organization}>
          {function (_a) {
                    var hasAccess = _a.hasAccess;
                    return (<react_1.Fragment>
              <StyledDropdownLink caret={false} customTitle={<button_1.default label={locale_1.t('Actions')} disabled={deleted} icon={<icons_1.IconEllipsis size="sm"/>}/>} anchorRight>
                <tooltip_1.default disabled={hasRole} title={noPermissionToDownloadDebugFilesInfo}>
                  <menuItemActionLink_1.default shouldConfirm={false} icon={<icons_1.IconDownload size="xs"/>} title={locale_1.t('Download')} href={downloadUrl} onClick={function (event) {
                            if (deleted) {
                                event.preventDefault();
                            }
                        }} disabled={!hasRole || deleted}>
                    {locale_1.t('Download')}
                  </menuItemActionLink_1.default>
                </tooltip_1.default>
                <tooltip_1.default disabled={hasAccess} title={noPermissionToDeleteDebugFilesInfo}>
                  <menuItemActionLink_1.default onAction={function () { return onDelete(debugFileId); }} message={debugFileDeleteConfirmationInfo} title={locale_1.t('Delete')} disabled={!hasAccess || deleted} shouldConfirm>
                    {locale_1.t('Delete')}
                  </menuItemActionLink_1.default>
                </tooltip_1.default>
              </StyledDropdownLink>
              <StyledButtonBar gap={1}>
                <tooltip_1.default disabled={hasRole} title={noPermissionToDownloadDebugFilesInfo}>
                  <button_2.default size="xsmall" icon={<icons_1.IconDownload size="xs"/>} href={downloadUrl} disabled={!hasRole}>
                    {locale_1.t('Download')}
                  </button_2.default>
                </tooltip_1.default>
                <tooltip_1.default disabled={hasAccess} title={noPermissionToDeleteDebugFilesInfo}>
                  <confirm_1.default confirmText={locale_1.t('Delete')} message={debugFileDeleteConfirmationInfo} onConfirm={function () { return onDelete(debugFileId); }} disabled={!hasAccess}>
                    <button_2.default priority="danger" icon={<icons_1.IconDelete size="xs"/>} size="xsmall" disabled={!hasAccess}/>
                  </confirm_1.default>
                </tooltip_1.default>
              </StyledButtonBar>
            </react_1.Fragment>);
                }}
        </access_1.default>);
        }}
    </role_1.default>);
    if (!deleted) {
        return actions;
    }
    return (<tooltip_1.default title={locale_1.t('Actions not available because this debug file was deleted')}>
      {actions}
    </tooltip_1.default>);
}
exports.default = Actions;
var StyledDropdownLink = styled_1.default(dropdownLink_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n    transition: none;\n  }\n"], ["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n    transition: none;\n  }\n"])), function (props) { return props.theme.breakpoints[4]; });
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (min-width: ", ") {\n    display: none;\n  }\n"])), function (props) { return props.theme.breakpoints[4]; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=actions.jsx.map