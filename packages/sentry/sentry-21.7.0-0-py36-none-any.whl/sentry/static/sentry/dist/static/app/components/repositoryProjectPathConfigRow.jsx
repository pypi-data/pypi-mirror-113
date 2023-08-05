Object.defineProperty(exports, "__esModule", { value: true });
exports.ButtonColumn = exports.InputPathColumn = exports.OutputPathColumn = exports.NameRepoColumn = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var RepositoryProjectPathConfigRow = /** @class */ (function (_super) {
    tslib_1.__extends(RepositoryProjectPathConfigRow, _super);
    function RepositoryProjectPathConfigRow() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RepositoryProjectPathConfigRow.prototype.render = function () {
        var _a = this.props, pathConfig = _a.pathConfig, project = _a.project, onEdit = _a.onEdit, onDelete = _a.onDelete;
        return (<access_1.default access={['org:integrations']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<react_1.Fragment>
            <exports.NameRepoColumn>
              <ProjectRepoHolder>
                <RepoName>{pathConfig.repoName}</RepoName>
                <ProjectAndBranch>
                  <idBadge_1.default project={project} avatarSize={14} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
                  <BranchWrapper>&nbsp;|&nbsp;{pathConfig.defaultBranch}</BranchWrapper>
                </ProjectAndBranch>
              </ProjectRepoHolder>
            </exports.NameRepoColumn>
            <exports.OutputPathColumn>{pathConfig.sourceRoot}</exports.OutputPathColumn>
            <exports.InputPathColumn>{pathConfig.stackRoot}</exports.InputPathColumn>
            <exports.ButtonColumn>
              <tooltip_1.default title={locale_1.t('You must be an organization owner, manager or admin to edit or remove a code mapping.')} disabled={hasAccess}>
                <StyledButton size="small" icon={<icons_1.IconEdit size="sm"/>} label={locale_1.t('edit')} disabled={!hasAccess} onClick={function () { return onEdit(pathConfig); }}/>
                <confirm_1.default disabled={!hasAccess} onConfirm={function () { return onDelete(pathConfig); }} message={locale_1.t('Are you sure you want to remove this code mapping?')}>
                  <StyledButton size="small" icon={<icons_1.IconDelete size="sm"/>} label={locale_1.t('delete')} disabled={!hasAccess}/>
                </confirm_1.default>
              </tooltip_1.default>
            </exports.ButtonColumn>
          </react_1.Fragment>);
            }}
      </access_1.default>);
    };
    return RepositoryProjectPathConfigRow;
}(react_1.Component));
exports.default = RepositoryProjectPathConfigRow;
var ProjectRepoHolder = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var RepoName = styled_1.default("span")(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding-bottom: ", ";\n"], ["\n  padding-bottom: ", ";\n"])), space_1.default(1));
var StyledButton = styled_1.default(button_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space_1.default(0.5));
var ProjectAndBranch = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  color: ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
// match the line height of the badge
var BranchWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  line-height: 1.2;\n"], ["\n  line-height: 1.2;\n"])));
// Columns below
var Column = styled_1.default('span')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  overflow-wrap: break-word;\n"], ["\n  overflow: hidden;\n  overflow-wrap: break-word;\n"])));
exports.NameRepoColumn = styled_1.default(Column)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  grid-area: name-repo;\n"], ["\n  grid-area: name-repo;\n"])));
exports.OutputPathColumn = styled_1.default(Column)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  grid-area: output-path;\n"], ["\n  grid-area: output-path;\n"])));
exports.InputPathColumn = styled_1.default(Column)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  grid-area: input-path;\n"], ["\n  grid-area: input-path;\n"])));
exports.ButtonColumn = styled_1.default(Column)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  grid-area: button;\n  text-align: right;\n"], ["\n  grid-area: button;\n  text-align: right;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=repositoryProjectPathConfigRow.jsx.map