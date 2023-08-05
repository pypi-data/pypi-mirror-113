Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var SourceMapsArchiveRow = function (_a) {
    var archive = _a.archive, orgId = _a.orgId, projectId = _a.projectId, onDelete = _a.onDelete;
    var name = archive.name, date = archive.date, fileCount = archive.fileCount;
    var archiveLink = "/settings/" + orgId + "/projects/" + projectId + "/source-maps/" + encodeURIComponent(name);
    return (<react_1.Fragment>
      <Column>
        <textOverflow_1.default>
          <link_1.default to={archiveLink}>
            <version_1.default version={name} anchor={false} tooltipRawVersion truncate/>
          </link_1.default>
        </textOverflow_1.default>
      </Column>
      <ArtifactsColumn>
        <count_1.default value={fileCount}/>
      </ArtifactsColumn>
      <Column>{locale_1.t('release')}</Column>
      <Column>
        <dateTime_1.default date={date}/>
      </Column>
      <ActionsColumn>
        <buttonBar_1.default gap={0.5}>
          <access_1.default access={['project:releases']}>
            {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<tooltip_1.default disabled={hasAccess} title={locale_1.t('You do not have permission to delete artifacts.')}>
                <confirm_1.default onConfirm={function () { return onDelete(name); }} message={locale_1.t('Are you sure you want to remove all artifacts in this archive?')} disabled={!hasAccess}>
                  <button_1.default size="small" icon={<icons_1.IconDelete size="sm"/>} title={locale_1.t('Remove All Artifacts')} label={locale_1.t('Remove All Artifacts')} disabled={!hasAccess}/>
                </confirm_1.default>
              </tooltip_1.default>);
        }}
          </access_1.default>
        </buttonBar_1.default>
      </ActionsColumn>
    </react_1.Fragment>);
};
var Column = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  overflow: hidden;\n"], ["\n  display: flex;\n  align-items: center;\n  overflow: hidden;\n"])));
var ArtifactsColumn = styled_1.default(Column)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding-right: ", ";\n  text-align: right;\n  justify-content: flex-end;\n"], ["\n  padding-right: ", ";\n  text-align: right;\n  justify-content: flex-end;\n"])), space_1.default(4));
var ActionsColumn = styled_1.default(Column)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
exports.default = SourceMapsArchiveRow;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sourceMapsArchiveRow.jsx.map