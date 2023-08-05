Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var commandLine_1 = tslib_1.__importDefault(require("app/components/commandLine"));
describe('CommandLine', function () {
    it('renders', function () {
        var children = 'sentry devserver --workers';
        var wrapper = enzyme_1.mountWithTheme(<commandLine_1.default>{children}</commandLine_1.default>);
        expect(wrapper.find('CommandLine').text()).toBe(children);
    });
});
//# sourceMappingURL=commandLine.spec.jsx.map