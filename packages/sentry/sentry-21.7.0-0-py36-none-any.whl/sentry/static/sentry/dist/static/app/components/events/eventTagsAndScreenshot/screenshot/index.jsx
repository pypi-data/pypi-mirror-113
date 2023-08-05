Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var role_1 = tslib_1.__importDefault(require("app/components/acl/role"));
var menuItemActionLink_1 = tslib_1.__importDefault(require("app/components/actions/menuItemActionLink"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var dataSection_1 = tslib_1.__importDefault(require("../dataSection"));
var imageVisualization_1 = tslib_1.__importDefault(require("./imageVisualization"));
var modal_2 = tslib_1.__importStar(require("./modal"));
function Screenshot(_a) {
    var event = _a.event, api = _a.api, organization = _a.organization, projectSlug = _a.projectSlug;
    var _b = tslib_1.__read(react_1.useState([]), 2), attachments = _b[0], setAttachments = _b[1];
    var _c = tslib_1.__read(react_1.useState(false), 2), isLoading = _c[0], setIsLoading = _c[1];
    var orgSlug = organization.slug;
    react_1.useEffect(function () {
        fetchData();
    }, []);
    function fetchData() {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var response, _err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!event) {
                            return [2 /*return*/];
                        }
                        setIsLoading(true);
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/events/" + event.id + "/attachments/")];
                    case 2:
                        response = _a.sent();
                        setAttachments(response);
                        setIsLoading(false);
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        // TODO: Error-handling
                        setAttachments([]);
                        setIsLoading(false);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function hasScreenshot(attachment) {
        var mimetype = attachment.mimetype;
        return mimetype === 'image/jpeg' || mimetype === 'image/png';
    }
    function handleDelete(screenshotAttachmentId, downloadUrl) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _err_2;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, api.requestPromise(downloadUrl.split('/api/0')[1], {
                                method: 'DELETE',
                            })];
                    case 1:
                        _a.sent();
                        setAttachments(attachments.filter(function (attachment) { return attachment.id !== screenshotAttachmentId; }));
                        return [3 /*break*/, 3];
                    case 2:
                        _err_2 = _a.sent();
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    }
    function handleOpenVisualizationModal(eventAttachment, downloadUrl) {
        modal_1.openModal(function (modalProps) { return (<modal_2.default {...modalProps} event={event} orgSlug={orgSlug} projectSlug={projectSlug} eventAttachment={eventAttachment} downloadUrl={downloadUrl} onDelete={function () { return handleDelete(eventAttachment.id, downloadUrl); }}/>); }, { modalCss: modal_2.modalCss });
    }
    function renderContent(screenshotAttachment) {
        var downloadUrl = "/api/0/projects/" + organization.slug + "/" + projectSlug + "/events/" + event.id + "/attachments/" + screenshotAttachment.id + "/";
        return (<react_1.Fragment>
        <StyledPanelBody>
          <imageVisualization_1.default attachment={screenshotAttachment} orgId={orgSlug} projectId={projectSlug} event={event}/>
        </StyledPanelBody>
        <StyledPanelFooter>
          <StyledButtonbar gap={1}>
            <button_1.default size="xsmall" onClick={function () {
                return handleOpenVisualizationModal(screenshotAttachment, downloadUrl + "?download=1");
            }}>
              {locale_1.t('View screenshot')}
            </button_1.default>
            <dropdownLink_1.default caret={false} customTitle={<button_1.default label={locale_1.t('Actions')} size="xsmall" icon={<icons_1.IconEllipsis size="xs"/>}/>} anchorRight>
              <menuItemActionLink_1.default shouldConfirm={false} title={locale_1.t('Download')} href={downloadUrl + "?download=1"}>
                {locale_1.t('Download')}
              </menuItemActionLink_1.default>
              <menuItemActionLink_1.default shouldConfirm title={locale_1.t('Delete')} onAction={function () { return handleDelete(screenshotAttachment.id, downloadUrl); }} header={locale_1.t('Screenshots help identify what the user saw when the event happened')} message={locale_1.t('Are you sure you wish to delete this screenshot?')}>
                {locale_1.t('Delete')}
              </menuItemActionLink_1.default>
            </dropdownLink_1.default>
          </StyledButtonbar>
        </StyledPanelFooter>
      </react_1.Fragment>);
    }
    return (<role_1.default role={organization.attachmentsRole}>
      {function (_a) {
            var hasRole = _a.hasRole;
            var screenshotAttachment = attachments.find(hasScreenshot);
            if (!hasRole || isLoading || !screenshotAttachment) {
                return null;
            }
            return (<dataSection_1.default title={locale_1.t('Screenshots')} description={locale_1.t('Screenshots help identify what the user saw when the event happened')}>
            <StyledPanel>{renderContent(screenshotAttachment)}</StyledPanel>
          </dataSection_1.default>);
        }}
    </role_1.default>);
}
exports.default = withApi_1.default(Screenshot);
var StyledPanel = styled_1.default(panels_1.Panel)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n  margin-bottom: 0;\n  min-height: 200px;\n  min-width: 175px;\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n  margin-bottom: 0;\n  min-height: 200px;\n  min-width: 175px;\n"])));
var StyledPanelBody = styled_1.default(panels_1.PanelBody)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: 175px;\n  overflow: hidden;\n  border: 1px solid ", ";\n  border-radius: ", ";\n  margin: -1px;\n  width: calc(100% + 2px);\n  border-bottom-left-radius: 0;\n  border-bottom-right-radius: 0;\n"], ["\n  height: 175px;\n  overflow: hidden;\n  border: 1px solid ", ";\n  border-radius: ", ";\n  margin: -1px;\n  width: calc(100% + 2px);\n  border-bottom-left-radius: 0;\n  border-bottom-right-radius: 0;\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; });
var StyledPanelFooter = styled_1.default(panels_1.PanelFooter)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  width: 100%;\n"], ["\n  padding: ", ";\n  width: 100%;\n"])), space_1.default(1));
var StyledButtonbar = styled_1.default(buttonBar_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  justify-content: space-between;\n  .dropdown {\n    height: 24px;\n  }\n"], ["\n  justify-content: space-between;\n  .dropdown {\n    height: 24px;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map