Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var progressBar_1 = tslib_1.__importDefault(require("app/components/progressBar"));
describe('ProgressBar', function () {
    it('basic', function () {
        var progressBarValue = 50;
        var wrapper = enzyme_1.mountWithTheme(<progressBar_1.default value={progressBarValue}/>);
        // element exists
        expect(wrapper.length).toEqual(1);
        var elementProperties = wrapper.find('div').props();
        expect(elementProperties).toHaveProperty('role', 'progressbar');
        // check aria attributes
        expect(elementProperties).toHaveProperty('aria-valuenow', progressBarValue);
        expect(elementProperties).toHaveProperty('aria-valuemin', 0);
        expect(elementProperties).toHaveProperty('aria-valuemax', 100);
    });
});
//# sourceMappingURL=progressBar.spec.jsx.map