Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var createProject_1 = tslib_1.__importDefault(require("app/views/projectInstall/createProject"));
var NewProject = function () { return (<Container>
    <div className="container">
      <Content>
        <react_document_title_1.default title="Sentry"/>
        <createProject_1.default />
      </Content>
    </div>
  </Container>); };
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  background: ", ";\n  margin-bottom: -", "; /* cleans up a bg gap at bottom */\n"], ["\n  flex: 1;\n  background: ", ";\n  margin-bottom: -", "; /* cleans up a bg gap at bottom */\n"])), function (p) { return p.theme.background; }, space_1.default(3));
var Content = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(3));
exports.default = NewProject;
var templateObject_1, templateObject_2;
//# sourceMappingURL=newProject.jsx.map